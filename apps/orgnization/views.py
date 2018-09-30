#_*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from orgnization.models import CourseOrg,CityDict,Teacher
from operatioon.models import UserFavorite,Course
from .forms import UserAskForm
from users.forms import LoginForm
# Create your views here


class OrgView(View):
    def get(self,request):
        all_citys=CityDict.objects.all()
        all_orgs=CourseOrg.objects.all()
        hot_orgs=all_orgs.order_by('-click_nums')[:3]
        org_nums= all_orgs.count()
        #获取城市的id筛选
        city_id=request.GET.get('city','')
        #获取机构
        category=request.GET.get('ct','')
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))
        if category:
            all_orgs=all_orgs.filter(category=category)
            # 搜索相关讲师
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        #排序
        sort=request.GET.get('sort','')
        if sort:
            if sort=='students':
                all_orgs=all_orgs.order_by("-students")
            if sort=='courses':
                all_orgs=all_orgs.order_by('-click_nums')
        #对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs,3, request=request)
        orgs = p.page(page)
        return render(request,'org-list.html',{
            'all_citys':all_citys,
            'all_orgs':orgs,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort

        })


class AddUserAsView(View):
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
              user_ask=userask_form.save(commit=True)
              return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
              print ('haha')
              return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type="application/json")


class OrgHomeview(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        curent_page='home'
        course_org=CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums+=1
        course_org.save()
        all_courses=course_org.course_set.all()[:3]
        all_teachers=course_org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-homepage.html',{'all_courses':all_courses,'all_teachers':all_teachers,'course_org':course_org,'curent_page':curent_page,'has_fav':has_fav})


class OrgCourseview(View):
    '''
    机构课程列表页
    '''

    def get(self, request, org_id):
        curent_page='course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html',
                      {'all_courses': all_courses,'course_org': course_org,'curent_page':curent_page,'has_fav':has_fav})


class OrgDescview(View):
   '''
   机构描述
   '''

   def get(self, request, org_id):
       curent_page = 'desc'
       course_org = CourseOrg.objects.get(id=int(org_id))
       has_fav = False
       if request.user.is_authenticated():
           if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
               has_fav = True
       return render(request, 'org-detail-desc.html',
                     {'course_org': course_org, 'curent_page': curent_page,'has_fav':has_fav})


class OrgTeacherview(View):
    '''
    机构讲师
    '''
    def get(self,request,org_id):
        curent_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav=False
        if request.user.is_authenticated():
          if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
              has_fav=True
        return render(request, 'org-detail-teachers.html',
                      {'course_org': course_org, 'curent_page': curent_page,'all_teachers':all_teachers,'has_fav':has_fav})


class AddFavView(View):
    '''
    用户收藏
    '''
    def post(self,request):
          fav_id=request.POST.get('fav_id',0)
          fav_type=request.POST.get('fav_type',0)
          if not request.user.is_authenticated():
              #判断用户登录状态
              return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")
          exist_userfav=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
          if exist_userfav:
              exist_userfav.delete()
              if int(fav_type)==1:
                  course=Course.objects.get(id=int(fav_id))
                  course.fav_nums-=1
                  if course.fav_nums<0:
                      course.fav_nums=0
                  course.save()
              elif int(fav_type)==2:
                  courseorg=CourseOrg.objects.get(id=int(fav_id))
                  courseorg.fav_nums-=1
                  if courseorg.fav_nums<0:
                      courseorg.fav_nums=0
                  courseorg.save()
              elif int(fav_type)==3:
                  teacher=Teacher.objects.filter(id=int(fav_id))
                  teacher.fav_nums-=1
                  if teacher.fav_nums < 0:
                      teacher.fav_nums = 0
                  teacher.save()
              return HttpResponse('{"status":"success","msg":"收藏"}',content_type="application/json")
          else:
              userfav=UserFavorite()
              if int(fav_id)>0 and int(fav_type>0):
                  userfav.user=request.user
                  userfav.fav_id=int(fav_id)
                  userfav.fav_type=int(fav_type)
                  userfav.save()
                  if int(fav_type) == 1:
                      course = Course.objects.get(id=int(fav_id))
                      course.fav_nums+= 1
                      course.save()
                  elif int(fav_type) == 2:
                      courseorg = CourseOrg.objects.get(id=int(fav_id))
                      courseorg.fav_nums+= 1
                      courseorg.save()
                  elif int(fav_type) == 3:
                      teacher = Teacher.objects.filter(id=int(fav_id))
                      teacher.fav_nums+= 1
                      teacher.save()
                  return HttpResponse('{"status":"success","msg":"已收藏"}', content_type="application/json")
              else:
                  return HttpResponse('{"status":"fail","msg":"收藏失败"}', content_type="application/json")


class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self,request):
        all_teachers=Teacher.objects.all()
        all_teachers_nums=all_teachers.count()
        sort = request.GET.get('sort', '')
        # 搜索相关讲师
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                work_position__icontains=search_keywords))
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by("-click_nums")
        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)
        sort_teacher=Teacher.objects.all()[:3]
        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'sort_teacher':sort_teacher,
            'all_teachers_nums':all_teachers_nums,
            'sort':sort
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher=Teacher.objects.filter(id=teacher_id).first()
        teacher.click_nums+=1
        teacher.save()
        all_courses=Course.objects.filter(teacher=teacher)
        sort_teacher=Teacher.objects.all()[:3]
        has_teacher_fav=False
        has_org_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
                has_teacher_fav=True
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org_id):
                has_org_fav=True
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':all_courses,
            'sort_teacher':sort_teacher,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav
        })









