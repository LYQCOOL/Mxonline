# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/7/31 21:07'
import xadmin

from .models import *
from orgnization.models import CourseOrg


class LessonInline(object):
    model=Lesson
    extra=0


class CourseResourceInline(object):
    model=CourseResource
    extra=0


# class VideoInline(object):
#     model=Video
#     extra=0


class CourseAdmin(object):
    list_display=['name','course_org','desc','detail','is_banner','teacher','degree','learn_times','students','fav_nums','image','click_nums','category','tag','youneed_know','teacher_tell','add_time','get_zj_nums']
    search_fields=['course_org','name','desc','detail','is_banner','teacher','degree','learn_times','students','fav_nums','image','click_nums','category','tag','youneed_know','teacher_tell']
    list_filter=['course_org','name','desc','detail','is_banner','teacher','degree','learn_times','students','fav_nums','image','click_nums','category','tag','youneed_know','teacher_tell','add_time']
    #配置默认排序规则
    ordering=['-click_nums']
    #设置未只读，不能修改
    readonly_fields=['click_nums']
    #设置为后台不能看见,与readony_fields冲突，有前者，exclude不生效
    exclude=['fav_nums']
    # 设置添加时可以搜索，而不是下拉框，ajax加载(外键)
    # relfield_style = 'fk-ajax'
    #在同一个页面添加完整数据,不可以在在章节中嵌套视频，但可以多个
    inlines=[LessonInline,CourseResourceInline]
    #列表页直接修改的字段
    list_editable=['degree','desc']
    #设置后台列表刷新时间
    refresh_times=[3,5]
    #定义样式
    style_fields={"detail":"ueditor"}
    # relfield_style='fk-ajax'
    #导入excel插件
    import_excel = True

    # 筛选不是轮播图的数据
    def queryset(self):
        #调用当前的admin
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    #统计课程数
    def save_models(self):
        '''
        在保存课程时统计课程机构的课程数
        '''
        obj=self.new_obj
        obj.save()
        course_org=obj.course_org
        if course_org is not None:
            course_org.course_nums=Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        #必须返回，不然报错（或者注释掉）
        return super(CourseAdmin,self).post(request,*args,**kwargs)

class BannerCourseAdmin(object):
    list_display=['name','course_org','desc','detail','is_banner','teacher','degree','learn_times','students','fav_nums','image','click_nums','category','tag','youneed_know','teacher_tell','add_time']
    search_fields=['course_org','name','desc','detail','is_banner','teacher','degree','learn_times','students','fav_nums','image','click_nums','category','tag','youneed_know','teacher_tell']
    list_filter=['course_org','name','desc','detail','is_banner','teacher','degree','learn_times','students','fav_nums','image','click_nums','category','tag','youneed_know','teacher_tell','add_time']
    #配置默认排序规则
    ordering=['-click_nums']
    #设置未只读，不能修改
    readonly_fields=['click_nums']
    #设置为后台不能看见,与readony_fields冲突，有前者，exclude不生效
    exclude=['fav_nums']
    # 设置添加时可以搜索，而不是下拉框，ajax加载(外键)
    # relfield_style = 'fk-ajax'
    #在同一个页面添加完整数据,不可以在在章节中嵌套视频，但可以多个
    inlines=[LessonInline,CourseResourceInline]

    #筛选为轮播图的数据
    def queryset(self):
        qs=super(BannerCourseAdmin,self).queryset()
        qs=qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display=['course','name','learn_times','add_time']
    search_fields=['course','name','learn_times']
    list_filter=['course__name','name','learn_times','add_time']
    # inlines=[VideoInline]


class VideoAdmin(object):
    list_dispaly=['lesson','name','learn_times','url','add_time']
    search_fields=['lesson','name','learn_times','url']
    list_filter=['lesson__name','name','learn_times','url','add_time']


class CourseResourceAdmin(object):
    list_dispaly = ['course', 'name', 'download','add_time']
    search_fields =['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download','add_time']
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)