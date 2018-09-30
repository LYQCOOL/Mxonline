# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/2 20:06'
from random import Random

from django.core.mail import send_mail
from Mxonline.settings import EMAIL_FROM

from users.models import EmailVeriyRecord

def random_str(randomlength=8):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length=len(chars)-1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str



def send_register_email(email,send_type='register'):
    email_record=EmailVeriyRecord()
    if send_type=='update_email':
        code=random_str(4)
    else:
        code=random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()
    if send_type=='register':
        email_title='Seven_Lucky_Number程序网注册激活'
        email_body='请点击下面的链接注册激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type=='forget':
        email_title = 'Seven_Lucky_Number密码找回'
        email_body = '请点击下面的链接找回你的账号：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type=='update_email':
        email_title = 'Seven_Lucky_Number邮箱验证码修改'
        email_body = '您的邮箱验证码为：{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass