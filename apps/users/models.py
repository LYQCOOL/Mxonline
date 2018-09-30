#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.


class User(AbstractUser):
    nick_name=models.CharField(max_length=50,verbose_name=u'昵称',default='')
    birthday=models.DateField(verbose_name=u'生日',null=True,blank=True)
    genter=models.CharField(choices=(('male',u'男'),('fmale',u'女')),verbose_name='性别',default='male',max_length=10)
    address=models.CharField(max_length=100,default=u'')
    mobile=models.CharField(max_length=11,null=True,blank=True)
    image=models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png',max_length=100)


    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name


    def __unicode__(self):
        return self.nick_name


    def unread_nums(self):
        '''
        获取用户未读消息
        :return: 
        '''
        from operatioon.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()


class EmailVeriyRecord(models.Model):
    code=models.CharField(max_length=50,verbose_name=u'验证码')
    email=models.EmailField(verbose_name=u'邮箱')
    send_type=models.CharField(choices=(('register','注册'),('forget','忘记密码'),('update_email','更新邮箱')),max_length=20)
    send_time=models.DateTimeField(default=datetime.now)


    class Meta:
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name


    def __unicode__(self):
            return '{0}({1})'.format(self.code,self.email)


class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name=u'标题')
    image=models.ImageField(max_length=100,verbose_name=u'轮播图')
    url=models.URLField(max_length=200,verbose_name=u'网址')
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name='轮播图'
        verbose_name_plural=verbose_name


    def __unicode__(self):
        return self.title