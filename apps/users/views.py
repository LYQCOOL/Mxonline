# _*_ coding:utf-8 _*_
import json

from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from users.models import User,EmailVeriyRecord
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operatioon.models import UserCourse,UserFavorite,Course,UserMessage
from orgnization.models import CourseOrg,Teacher
from .models import Banner
# Create your views here.


class CustomBackend(ModelBackend):
   '''
   自定义用户验证
   '''
   def authenticate(self, username=None, password=None, **kwargs):
       try:
           user=User.objects.get(Q(username=username)|Q(email=username))
           user.check_password(password)
           return user
       except Exception as e:
           return None


class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name=request.POST.get('email','')
            if User.objects.filter(email=user_name):
                return render(request,'register.html',{'msg':'该用户已经存在！！','register_form':register_form})
            pwd=request.POST.get('password','')
            new_user=User()
            new_user.username=user_name
            new_user.email=user_name
            new_user.is_active=False
            new_user.password=make_password(pwd)
            new_user.save()
            user_message=UserMessage()
            user_message.user=new_user
            user_message.message='欢迎注册慕学在线网'
            user_message.save()
            send_register_email(user_name,'register')
            return render(request,'login.html',{'msg':'注册成功'})
        else:
            return render(request,'register.html',{'register_form':register_form})


class ActiveView(View):
    def get(self,request,active_code):
        all_record=EmailVeriyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email=record.email
                user=User.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


class ResetView(View):
    def get(self,request,active_code):
        all_record=EmailVeriyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email=record.email
                return render(request, 'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')


class ModifyPwdView(View):
    '''
    未登录修改密码
    '''
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1','')
            pwd2=request.POST.get('password2','')
            email=request.POST.get('email','')
            if pwd1!=pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致！'})
            user=User.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()
            return render(request,'login.html')
        else:
            return render(request,'password_reset.html',{'modify_form':modify_form})


class LoginView(View):
    def get(self,request):
        return render(self.request, 'login.html')
    def post(self,request):
        loginform=LoginForm(request.POST)
        if loginform.is_valid():
            user_name = request.POST.get('username', '')
            pwd = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    # 重定向
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request,'login.html',{'msg':'用户未激活！！','loginform':loginform})
            else:
                return render(request, 'login.html', {'msg':'用户名或密码错误！！'})
        else:
            return render(request, 'login.html', {'loginform':loginform})


# class LoginUnsaveView(View):
#     '''
#     演示sql注入攻击web网站，登录时邮箱输入'OR 1=1#(使sql语句为真，即查询到)
#     '''
#
#
#     def get(self, request):
#         return render(self.request, 'login.html')
#
#
#     def post(self, request):
#         user_name = request.POST.get('username', '')
#         pwd = request.POST.get('password', '')
#         import MySQLdb
#         conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='112358',db='mxonline',charset='utf8')
#         cursor=conn.cursor()
#         sql_select="select * from users_user WHERE email='{0}' and password='{1}'".format(user_name,pwd)
#         result=cursor.execute(sql_select)
#         for row in result:
#            print('成功')

# def user_login(request):
#     if request.method=='POST':
#          user_name=request.POST.get('username','')
#          pwd=request.POST.get('password','')
#          user=authenticate(username=user_name,password=pwd)
#          if user is not None:
#              login(request,user)
#              return render(request,'index.html')
#          else:
#              return render(request,'login.html',{'msg':u'用户名或密码错误！！'})
#     elif request.method=='GET':
#         return render(request,'login.html')


class ForgetView(View):
    def get(self,request):
       forget_form=ForgetForm()
       return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request, 'sendsuccess.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


class LogoutView(View):
    def get(self,request):
        #调用django的logout函数
        logout(request)
        #反解url
        from django.core.urlresolvers import reverse
        #重定向
        return HttpResponseRedirect(reverse('index'))


class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"failure","msg":"字段不符合规范！"}',content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    '''
    上传用户头像
    '''
    def post(self,request):
       image_form=UploadImageForm(request.POST,request.FILES,instance=request.user)
       if image_form.is_valid():
           #直接利用Modelform保存
           image_form.save()
           return HttpResponse('{"status":"success"}', content_type="application/json")
           #获取对象保存
           # image=image_form.cleaned_data['image']
           # request.user.image=image
           # request.user.save()
       else:
           return HttpResponse('{"status":"fail"}', content_type="application/json")


class UpdatePwdView(View):
    '''
    个人中心修改密码
    '''
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1','')
            pwd2=request.POST.get('password2','')
            if pwd1!=pwd2:
                return HttpResponse('{"status":"fail","msg":"两次密码不一致！！"}',content_type='application/json')
            user=request.user
            user.password=make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success","msg":"修改成功！！"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    发送个人邮箱验证码
    '''
    def get(self,request):
       email=request.GET.get('email','')
       if User.objects.filter(email=email):
           return HttpResponse('{"email":"邮箱已经存在"}',content_type='application/json')
       else:
           send_register_email(email,'update_email')
           return HttpResponse('{"status":"success"}',content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改个人邮箱
    '''
    def post(self,request):
        email=request.POST.get('email','')
        code=request.POST.get('code','')
        exsited_records=EmailVeriyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if exsited_records:
           user=request.user
           user.email=email
           user.save()
           return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}',content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    '''
    我的课程
    '''
    def get(self,request):
        courses=UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'courses':courses
        })


class FavOrgView(LoginRequiredMixin,View):
    '''
    课程收藏
    '''
    def get(self,request):
        org_list=[]
        fav_orgs=UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org=CourseOrg.objects.filter(id=fav_org.fav_id).first()
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            "org_list":org_list
        })


class FavTeacherView(LoginRequiredMixin,View):
    '''
    讲师收藏
    '''
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.filter(id=fav_teacher.fav_id).first()
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list
        })


class FavCourseView(LoginRequiredMixin,View):
    '''
    课程收藏
    '''
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course = Course.objects.filter(id=fav_course.fav_id).first()
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list
        })


class MyMessageView(LoginRequiredMixin,View):
    '''
    我的消息
    '''
    def get(self,request):
        all_message=UserMessage.objects.filter(user=request.user.id)
        allunread_message=UserMessage.objects.filter(user=request.user.id,has_read=False)
        #用户进入个人消息后清空未读
        for unread_message in allunread_message:
            unread_message.has_read=True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_message, 3, request=request)
        messages = p.page(page)
        return render(request,'usercenter-message.html',{
            'messages':messages
        })


class IndexView(View):
    '''
    主页面
    '''
    def get(self,request):
        '''
        取出轮播图
        '''
        #print 1/0服务器出错
        all_banners=Banner.objects.all().order_by('index')
        courses=Course.objects.filter(is_banner=False)[:6]
        banner_courses=Course.objects.filter(is_banner=True)[:3]
        courseorgs=CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'courseorgs':courseorgs
        })


def page_not_found(request):
    '''
    全局404处理函数
    '''
    from django.shortcuts import render_to_response
    response=render_to_response('404.html',{})
    response.status_code=404
    return response


def page_error(request):
    '''
    全局500处理函数
    '''
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response