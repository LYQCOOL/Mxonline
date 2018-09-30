# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/5 16:07'
from django.conf.urls import url


from orgnization.views import *


urlpatterns=[
    url('^list/',OrgView.as_view(),name='org_list'),
    url('^add_ask/',AddUserAsView.as_view(),name='add_ask'),
    url('^home/(?P<org_id>\d+)/$',OrgHomeview.as_view(),name='org_home'),
    url('^course/(?P<org_id>\d+)/$', OrgCourseview.as_view(), name='org_course'),
    url('^desc/(?P<org_id>\d+)/$', OrgDescview.as_view(), name='org_desc'),
    url('^org_teacher/(?P<org_id>\d+)/$', OrgTeacherview.as_view(), name='org_teacher'),
    url('^add_fav/$',AddFavView.as_view(),name='add_fav'),
    url('^teacher/list/$',TeacherListView.as_view(),name='teacher_list'),
    #讲师详情页
    url('^teacher_detail/(?P<teacher_id>\d+)/$',TeacherDetailView.as_view(),name='teacher_detail')
]