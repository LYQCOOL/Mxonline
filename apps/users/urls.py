# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/14 11:07'
from django.conf.urls import url
from users.views import *
urlpatterns=[
    #用户信息
    url('^info/$',UserInfoView.as_view(),name='user_info'),
    #用户头像上传
    url('^image/upload/$',UploadImageView.as_view(),name='upload_image'),
    #用户个人中心修改密码
    url('^update/pwd/$',UpdatePwdView.as_view(),name='update_pwd'),
    #发送邮箱验证码修改邮箱
    url('^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    #修改邮箱
    url('^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    #我的课程
    url('^mycourse/$',MyCourseView.as_view(),name='mycourse'),
    #我的课程机构收藏
    url('^fav/org/$', FavOrgView.as_view(), name='my_fav_org'),
    # 我的授课讲师收藏
    url('^fav/teacher/$', FavTeacherView.as_view(), name='my_fav_teacher'),
    # 我的公开课收藏
    url('^fav/course/$', FavCourseView.as_view(), name='my_fav_course'),
    # 我的消息
    url('^mymessage/$', MyMessageView.as_view(), name='my_message'),

]