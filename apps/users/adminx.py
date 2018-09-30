# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/7/31 20:35'

import xadmin
from xadmin import views
# from xadmin.plugins.auth import UserAdmin
# from users.models import User

from .models import EmailVeriyRecord,Banner

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title='学习在线网后台管理'
    site_footer='七七大公司'
    menu_style='accordion'




# class UserAdmin(UserAdmin):
#     '''
#     注册User到用户管理
#     '''
#     pass


class EmailVeriyRecordAdmin(object):

    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']
    model_icon='fa fa-address-book'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'add_time']
    search_fields = ['title', 'image', 'url']
    list_filter = ['title', 'image', 'url', 'add_time']
    model_icon='fa fa-camera'
#卸载后台自带User注册
# from django.contrib.auth.models import User as us
# xadmin.site.unregister(us)
xadmin.site.register(EmailVeriyRecord,EmailVeriyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)
# xadmin.site.register(User,UserAdmin)