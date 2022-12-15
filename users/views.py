# Create your views here.
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc

from users.models import User
from utils.email import *
from utils.token import create_token
from utils.token import check_token
from .models import User


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        # print(username)
        # print(password1)
        # print(password2)
        # print(email)
        same_name_user = User.objects.filter(username=username)
        if same_name_user:
            return JsonResponse({'status_code': 2, 'message': '用户名已存在!'})

        same_email_user = User.objects.filter(email=email)
        if same_email_user:
            return JsonResponse({'status_code': 3, 'message': '该邮箱已被注册!'})

        # 检测密码不符合规范：8-18，英文字母+数字
        if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
            return JsonResponse({'status_code': 4, 'message': '密码不符合规范!'})

        if password1 != password2:
            return JsonResponse({'status_code': 5, 'message': '两次输入密码不一致!'})

        # success
        new_user = User()
        new_user.username = username
        new_user.password = hash_code(password1)
        new_user.email = email
        new_user.brief_intro = '这个人很懒，什么也没写'
        new_user.avatar = 'https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/yonghutouxiang/Transparent_Akkarin.jpg'
        new_user.save()

        code = make_confirm_string(new_user)
        try:
            send_email_confirm(email, code)
        except:
            new_user.delete()
            return JsonResponse({'status_code': 6, 'message': '验证邮件发送失败，请稍后再试!'})

        return JsonResponse({'status_code': 1, 'message': '注册成功，一封验证邮件已经发到您的邮箱，请点击链接进行确认!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.filter(username=username).first()
        except:
            return JsonResponse({'status_code': 3, 'message': '未查询到此用户!'})

        if user.password == hash_code(password):
            if not user.has_confirmed:
                return JsonResponse({'status_code': 5, 'message': '用户未确认，请前往邮箱确认!'})
            token = create_token(username)
            return JsonResponse({'status_code': 1, 'username': username, 'token': token, 'message': '登录成功!'})
        else:
            return JsonResponse({'status_code': 4, 'message': '密码错误!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            user = User.objects.filter(username=username).first()
        except:
            return JsonResponse({'status_code': 3, 'message': '没有这个用户哦'})
        if user.password == hash_code(old_password):
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
                return JsonResponse({'status_code': 4, 'message': '密码不符合规范'})
            if password1 != password2:
                return JsonResponse({'status_code': 5, 'message': '两次输入的新密码不一致'})
            user.password = hash_code(password1)
            user.save()
            return JsonResponse({'status_code': 1, 'message': '密码修改成功'})
        else:
            return JsonResponse({'status_code': 2, 'message': '密码错误!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            return JsonResponse({'status_code': 2})
        c_time = confirm.c_time.replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse({'status_code': 3})
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'status_code': 1})
    return JsonResponse({'status_code': -1})


@csrf_exempt
def get_userinfo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.filter(username=username).first()
            return JsonResponse(
                {'status_code': 1, 'avatar': user.avatar, 'email': user.email, 'brief_intro': user.brief_intro,
                 'gender': user.gender, 'phoneNumber': user.phoneNumber,
                 'organization': user.organization, 'realName': user.realName, 'userDegree': user.userDegree,
                 'authorID': user.authorID})
        except:
            return JsonResponse({'status_code': 2, 'message': '查无此人'})
    else:
        return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def update_info(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        avatar = request.POST.get('avatar')
        gender = request.POST.get('gender')
        
        phoneNumber = request.POST.get('phoneNumber')
        brief_intro = request.POST.get('brief_intro')
        organization = request.POST.get('organization')
        realName = request.POST.get('realName')
        userDegree = request.POST.get('userDegree')
        try:
            user = User.objects.filter(username=username).first()
        except:
            return JsonResponse({'status_code': 2, 'message': '查无此人!'})
        user.avatar = avatar
        user.gender = gender
        user.phoneNumber = phoneNumber
        user.brief_intro = brief_intro
        user.organization = organization
        user.realName = realName
        user.userDegree = userDegree
        user.save()
        return JsonResponse({'status_code': 1, 'message': '用户信息更新成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})

@csrf_exempt
def get_all(request):
    if request.method == 'POST':
        ans_list = []
        users=User.objects.all()
        for user in users:
            a={'id':user.id,'username':user.username}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})

@csrf_exempt
def get_one(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        try:
            user = User.objects.filter(username=username).first()
            return JsonResponse({'status_code': 1, 'message': user.id})
        except:
            return JsonResponse({'status_code': 3, 'message': '未查询到此用户!'})
        
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})