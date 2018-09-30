# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/7/31 21:36'
import xadmin


from .models import *


class CityDictAdmin(object):
    list_display=['name','desc','add_time']
    search_fileds=['name','desc']
    list_filter=['name','desc','add_time']
    model_icon='fa fa-home'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'tag','category','click_nums','fav_nums','image','address','city','students','students','course_nums','add_time']
    search_fileds = ['name', 'desc', 'tag','category','click_nums','fav_nums','image','address','city__name','students','students','course_nums','add_time']
    list_filter = ['name', 'desc', 'tag','category','click_nums','fav_nums','image','address','city__name','students','students','course_nums']
    model_icon='fa fa-university'
    #设置添加时可以搜索，而不是下拉框，ajax加载(外键)
    relfield_style='fk-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years','work_company','work_position','points','click_nums','fav_nums','age','add_time']
    search_fileds = ['org', 'name', 'work_years','work_company','work_position','points','click_nums','fav_nums','age']
    list_filter =['org__name', 'name', 'work_years','work_company','work_position','points','click_nums','fav_nums','age','add_time']
    model_icon='fa fa-user-o'
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)