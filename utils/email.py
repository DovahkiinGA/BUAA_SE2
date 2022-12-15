from django.conf import settings

from users.models import ConfirmString
from utils.hash import *

import datetime


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_email_confirm(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自知道了喵的注册确认邮件'

    text_content = '''感谢您的注册，这里是知道了喵，专注于团队协作与管理！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                       <p>感谢注册<a href="{}/confirm?code={}" target=blank>知道了喵</a>，\
                       相信的心就是你的魔法！</p>
                       <p>以上链接是进入知道了喵的邀请函，快来加入我们，成为猫娘神教的一员吧！</p>
                       <p>此邀请函有效期为{}天哦！</p>
                       '''.format(settings.FRONTEND, code, settings.CONFIRM_DAYS)  # url must be corrected
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])

    msg.attach_alternative(html_content, "text/html")

    msg.send()
    print("start sending email");
