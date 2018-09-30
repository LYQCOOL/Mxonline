# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/7 11:07'
from django.conf.urls import url

from courses.views import *

urlpatterns = [

    url('^list/$',CourseListView.as_view(),name='course_list'),
    url('^detail/(?P<course_id>\d+)/$',CourseDetailVIew.as_view(),name='course_detail'),
    #课程视频详情
    url('^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info'),
    #课程评论
    url('^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url('^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    #访问视频
    url('^video/(?P<video_id>\d+)/$', VideoView.as_view(), name='course_video'),

]