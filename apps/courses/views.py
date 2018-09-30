# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import *
from operatioon.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    '''
    课程展示
    '''
    def get(self,request):
        courses=Course.objects.all().order_by('-add_time')
        sort=request.GET.get('sort','')
        hot_courses=Course.objects.all().order_by('-click_nums')[:3]
        #搜索相关课程
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            courses=courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))
        #可程排序
        if sort:
            if sort=='students':
                courses=courses.order_by("-students")
            if sort=='hot':
                courses=courses.order_by('-click_nums')
        #课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(courses, 3, request=request)
        courses = p.page(page)
        return render(request,'course-list.html',{'courses':courses,'sort':sort,'hot_courses':hot_courses})


class CourseDetailVIew(View):
    '''
    课程详细信息
    '''
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        course.click_nums+=1
        course.save()
        has_favcourse=False
        has_favorg=False
        tag=course.tag
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_id,fav_type=1):
                has_favcourse=True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                has_favorg=True
        if tag:
            relate_course=Course.objects.filter(tag=tag).exclude(id=course.id).first()
        else:
            relate_course=None

        return render(request,'course-detail.html',{
            'cou':course,
            'relate_course':relate_course,
            'has_favcourse':has_favcourse,
            'has_favorg':has_favorg

        })


class CourseInfoView(LoginRequiredMixin,View):
    '''
    课程章节信息
    '''
    def get(self,request,course_id):
        courses=Course.objects.get(id=int(course_id))
        courses.students+=1
        courses.save()
        user_course=UserCourse.objects.filter(user=request.user,course=courses)
        if not user_course:
            user_course=UserCourse()
            user_course.user=request.user
            user_course.course=courses
            user_course.save()
        user_courses=UserCourse.objects.filter(course=courses)
        user_ids=[user_course.id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids).exclude(course=courses)
        #获取学过该课程的其他用户学过的其他课程
        courses_ids=[u_c.course.id for u_c in all_user_courses]
        relate_courses=Course.objects.filter(id__in=courses_ids).order_by('-click_nums')
        all_sources=CourseResource.objects.filter(course=courses)
        return render(request,'course-video.html',{
            'course_id':course_id,
            'courses':courses,
            'all_sources':all_sources,
            'relate_courses':relate_courses
        })


class CourseCommentView(LoginRequiredMixin,View):
    '''
    课程评论
    '''
    def get(self,request,course_id):
        courses=Course.objects.get(id=int(course_id))
        all_comments=CourseComments.objects.filter(course=courses)
        all_sources=CourseResource.objects.filter(course=courses)
        user_courses=UserCourse.objects.filter(course=courses)
        user_ids=[user_course.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=courses)
        # 获取学过该课程的其他用户学过的其他课程
        courses_ids = [u_c.course.id for u_c in all_user_courses]
        relate_courses = Course.objects.filter(id__in=courses_ids).order_by('-click_nums')
        return render(request,'course-comment.html',{
            'course_id':course_id,
            'courses':courses,
            'all_comments':all_comments,
            'all_sources': all_sources,
            'relate_courses': relate_courses
        })


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")
        course_id=request.POST.get('course_id',0)
        comments=request.POST.get('comments','')
        if course_id>0 and comments:
            course_comments=CourseComments()
            course=Course.objects.get(id=int(course_id))
            course_comments.course=course
            course_comments.comments=comments
            course_comments.user=request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type="application/json")


class VideoView(View):
    '''
    课程视频播放
    '''

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        courses = video.lesson.course
        courses.students += 1
        courses.save()
        user_course = UserCourse.objects.filter(user=request.user, course=courses)
        if not user_course:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = courses
            user_course.save()
        user_courses = UserCourse.objects.filter(course=courses)
        user_ids = [user_course.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course=courses)
        # 获取学过该课程的其他用户学过的其他课程
        courses_ids = [u_c.course.id for u_c in all_user_courses]
        relate_courses = Course.objects.filter(id__in=courses_ids).order_by('-click_nums')
        all_sources = CourseResource.objects.filter(course=courses)
        return render(request, 'course-play.html', {
            'courses': courses,
            'all_sources': all_sources,
            'relate_courses': relate_courses,
            'video':video
        })

