# Create your views here.
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc

from users.models import User
# from blog.models import UserInfo
# from blog.models import Article
from interact.models import Report, Apply
from utils.email import *
from utils.token import create_token
from utils.token import check_token
from message.models import Message
from scholar_data.models import Papers
from scholar_data.models import Authors


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
        new_user.isAdministrator = True
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
def get_info(request):
    if request.method == 'POST':
        user_num = User.objects.count()
        # 求门户数，不知道对不对
        gateway_num = Authors.objects.count()
        # 求门文章总数，不知道对不对
        article_num = Papers.objects.count()
        # 未审批的举报
        unsolve_reports = []
        for i in range(1, 5):
            unsolve_reports.append(Report.objects.filter(result=0, type=i))
        # 审批过的举报
        solved_reports = []
        for i in range(1, 5):
            solved_reports.append(Report.objects.exclude(result=0, type=i))
        unsolve_list = []
        solved_list = []
        for i in range(1, 5):
            temp_list = []
            for report in unsolve_reports[i - 1]:
                user = User.objects.filter(id=report.reporterID).first()
                dict = {
                    'reportID': report.id,
                    'reporterID': report.reporterID,
                    'username': user.username,
                    'avatar': user.avatar,
                    'objectID': report.objectID,
                    'content': report.content,
                    'reportTime': report.reportTime,
                    'result': report.result
                }
                temp_list.append(dict)
            if i == 1:
                unsolve_list.append({'articleReports': temp_list})
            elif i == 2:
                unsolve_list.append({'commentReports': temp_list})
            elif i == 3:
                unsolve_list.append({'postReports': temp_list})
            else:
                unsolve_list.append({'gatewayReports': temp_list})
        for i in range(1, 5):
            temp_list = []
            for report in solved_reports[i - 1]:

                user = User.objects.filter(id=report.reporterID).first()
                dict = {
                    'reportID': report.id,
                    'reporterID': report.reporterID,
                    'username': user.username,
                    'avatar': user.avatar,
                    'objectID': report.objectID,
                    'content': report.content,
                    'reportTime': report.reportTime,
                    'result': report.result
                }
                temp_list.append(dict)
            if i == 1:
                solved_list.append({'articleReports': temp_list})
            elif i == 2:
                solved_list.append({'commentReports': temp_list})
            elif i == 3:
                solved_list.append({'postReports': temp_list})
            else:
                solved_list.append({'gatewayReports': temp_list})
            return JsonResponse(
                {'status_code': 1, 'user_num': user_num, 'gateway_num': gateway_num, 'article_num': article_num,
                 'unsolve_reports': unsolve_list, 'solved_reports': solved_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def solve_report(request):
    if request.method == 'POST':
        reportID = request.POST.get('reportID')
        result = request.POST.get('result')
        report = Report.objects.filter(id=reportID).first()
        if report.result != 0:
            return JsonResponse({'status_code': 2, 'msg': '该举报已被处理'})
        report.result = result
        report.save()
        if result == "1":  # 发送成功邮件
            newMessage = Message()
            newMessage.senderID = 0
            newMessage.receiverID = report.reporterID
            newMessage.content = "举报成功"
            newMessage.type = 4
            newMessage.save()
        if result == "2":
            newMessage = Message()
            newMessage.senderID = 0
            newMessage.receiverID = report.reporterID
            newMessage.content = "举报失败"
            newMessage.type = 5
            newMessage.save()

        return JsonResponse({'status_code': 1, 'msg': '处理举报成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showApplication(request):
    if request.method == 'POST':
        applications = Apply.objects.filter(status=0)
        ans_list = []
        for application in applications:
            a = {
                'applicationID': application.id,
                'username': User.objects.filter(id=application.userID).first().username,
                'content': application.content,
                'authorID': application.authorID,
                'applyTime': application.applyTime
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def acceptApplication(request):
    if request.method == 'POST':
        applicationID = request.POST.get('applicationID')
        application = Apply.objects.filter(id=applicationID).first()
        application.status = 1
        application.save()
        # todo:给申请的用户发通过消息

        return JsonResponse({'status_code': 1, 'msg': '门户认领已通过'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def refuseApplication(request):
    if request.method == 'POST':
        applicationID = request.POST.get('applicationID')
        application = Apply.objects.filter(id=applicationID).first()
        application.status = 2
        application.save()
        # todo:给申请的用户发通过消息

        return JsonResponse({'status_code': 1, 'msg': '门户认领已拒绝'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})
