# _*_ encoding: utf-8 _*_
"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

from Mxonline.settings import MEDIA_ROOT
from users.views import LoginView,RegisterView,LogoutView,ActiveView,ForgetView,ResetView,ModifyPwdView,IndexView
import orgnization
from orgnization.views import OrgView
import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^login/',LoginView.as_view(),name='login'),
    #演示sql注入攻击web（不安全）
    # url(r'^login/',LoginUnsaveView.as_view(),name='login'),
    url(r'^register/',RegisterView.as_view(),name='register'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveView.as_view(),name='user_active_code'),
    url(r'^forgetpassword/',ForgetView.as_view(),name='forgetpwd'),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name='reset_code'),
    url(r'^modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    #课程机构配置
    url(r'^org/',include('orgnization.urls',namespace='org')),
    #配置上传文件访问的处理函数
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
    #DEBUG=False，static失效，django不管理静态文件
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    #课程相关配置
    url(r'^course/',include('courses.urls',namespace='course')),
    url(r'^users/', include('users.urls', namespace='user')),
    #富文本相关url（DjangoUeditor）
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

]
#全局404配置
handler404='users.views.page_not_found'
