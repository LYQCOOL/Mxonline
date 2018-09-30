# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/7/31 21:28'
import xadmin

from .models import *


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields =['user', 'course', 'comments']
    list_filter =['user__nick_name', 'course__name', 'comments', 'add_time']
    model_icon='fa fa-book'


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__nick_name', 'fav_id', 'fav_type', 'add_time']
    model_icon='fa fa-heart'


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    model_icon='fa fa-envelope'


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__nick_name', 'course__name', 'add_time']
    #配置后台图标
    model_icon='fa fa-mortar-board'


class UserAskAdmin(object):
    list_display=['name','mobile','course_name','add_time']
    search_fields=['name','mobile','course_name']
    list_filter=['name','mobile','course_name','add_time']
    model_icon='fa fa-question'

xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)