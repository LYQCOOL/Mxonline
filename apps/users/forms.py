# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/1 19:51'
from django import forms
from captcha.fields import CaptchaField

from .models import User

class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=5)
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误'})


class ForgetForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha=CaptchaField(error_messages={'invalid':u'验证码错误'})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['nick_name','genter','birthday','address','mobile']