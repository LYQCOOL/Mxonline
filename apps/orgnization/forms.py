# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/5 16:00'
import re
from django import forms

from operatioon.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']


    def clean_mobile(self):
        '''
        验证手机号码是否合法
        '''
        mobile=self.cleaned_data['mobile']
        REGIX='^1[3578][0-9]{9}$'
        p=re.compile(REGIX)
        if p.match(mobile):
            return mobile
        else:
            return forms.ValidationError(u'手机号码非法',code="mobile_invalid")