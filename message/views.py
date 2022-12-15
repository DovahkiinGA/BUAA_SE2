from django.shortcuts import render
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
# Create your views here.
from .models import *
from users.models import User
import datetime
from interact.models import CommentOnPost, CommentOnLiterature
from post.models import Post


@csrf_exempt
def sendNotice(request):
    if request.method == 'POST':

        receiverName = request.POST.get('receiver')
        receiver = User.objects.filter(username=receiverName).first()
        message = request.POST.get('message')
        if message == None:
            return JsonResponse({'status_code': 2, 'message': '请输入通知内容!'})
        if receiver == None:
            return JsonResponse({'status_code': 3, 'message': '发送通知的对象不存在!'})

        newMessage = Message()
        newMessage.senderID = 0
        newMessage.content = message
        newMessage.receiverID = receiver.id
        newMessage.type = 1
        newMessage.sendTime = datetime.datetime.now()
        newMessage.save()

        return JsonResponse({'status_code': 1, 'message': '通知发送成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def sendPersonalMessage(request):
    if request.method == 'POST':
        senderName = request.POST.get('sender')
        receiverName = request.POST.get('receiver')
        sender = User.objects.filter(username=senderName).first()
        receiver = User.objects.filter(username=receiverName).first()
        message = request.POST.get('message')
        if message == None:
            return JsonResponse({'status_code': 2, 'message': '请输入私信内容!'})
        if receiver == None:
            return JsonResponse({'status_code': 3, 'message': '发送私信的对象不存在!'})

        newMessage = Message()
        newMessage.content = message
        newMessage.senderID = sender.id
        newMessage.receiverID = receiver.id
        newMessage.sendTime = datetime.datetime.now()
        newMessage.type = 2
        newMessage.save()
        return JsonResponse({'status_code': 1, 'message': '私信发送成功喵!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def sendReplyInPost(request):
    if request.method == 'POST':
        senderName = request.POST.get('sender')
        receiverName = request.POST.get('receiver')
        postID = request.POST.get('postID')
        floor = request.POST.get('floor')
        sender = User.objects.filter(username=senderName).first()
        receiver = User.objects.filter(username=receiverName).first()
        post = Post.objects.filter(id=postID).first()
        message = request.POST.get('message')
        if message == None:
            return JsonResponse({'status_code': 2, 'message': '请输入回复内容!'})
        if receiver == None:
            return JsonResponse({'status_code': 3, 'message': '发送回复的对象不存在!'})
        # 给动态发表评论
        newComment = CommentOnPost()
        newComment.content = message
        newComment.postID = postID
        newComment.floor = post.floors + 1
        newComment.commentTime = datetime.datetime.now()
        newComment.userID = sender.id
        post.floors += 1
        post.save()
        newComment.save()

        # 给被回复人发消息
        newMessage = Message()
        newMessage.content = message
        newMessage.senderID = sender.id
        newMessage.receiverID = receiver.id
        newMessage.postID = postID
        newMessage.sendTime = datetime.datetime.now()
        newMessage.type = 3
        newMessage.save()
        return JsonResponse({'status_code': 1, 'message': '回复发送成功喵!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


# @csrf_exempt
# def sendReplyInLiterature(request):
#     if request.method == 'POST':
#         senderName = request.POST.get('sender')
#         receiverName = request.POST.get('receiver')
#         literatureID = request.POST.get('literatureID')
#         floor = request.POST.get('floor')
#         sender = User.objects.get(username=senderName)
#         receiver = User.objects.get(username=receiverName)
#         literature = Literature.objects.get(id=literatureID)
#         message = request.POST.get('message')
#         if message == None:
#             return JsonResponse({'status_code': 2, 'message': '请输入回复内容!'})
#         if receiver == None:
#             return JsonResponse({'status_code': 3, 'message': '发送回复的对象不存在!'})
#         # 给动态发表评论
#         newComment = CommentOnLiterature()
#         newComment.content = message
#         newComment.literatureID = literatureID
#         newComment.floor = literature.floors + 1
#         newComment.commentTime = datetime.datetime.now()
#         newComment.userID = sender.id
#         literature.floors += 1
#         literature.save()
#         newComment.save()
#
#         # 给被回复人发消息
#         newMessage = Message()
#         newMessage.content = message
#         newMessage.senderID = sender.id
#         newMessage.receiverID = receiver.id
#         newMessage.postID = postID
#         newMessage.sendTime = datetime.datetime.now()
#         newMessage.type = 3
#         newMessage.save()
#         return JsonResponse({'status_code': 1, 'message': '回复发送成功喵!'})
#     return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

@csrf_exempt
def viewMessage(request):
    if request.method == 'POST':
        messageID = request.POST.get('messageID')
        message = Message.objects.filter(id=messageID).first()
        message.viewed = True
        message.save()
        return JsonResponse({'status_code': 1, 'message': '消息已读'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userID = User.objects.filter(username=username).first().id
        messageList = Message.objects.filter(receiverID=userID).order_by('-sendTime')
        ans_list = []
        for message in messageList:
            user = User.objects.filter(id=message.senderID).first()
            a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                 'content': message.content, 'postID': message.postID, 'viewed': message.viewed,
                 'type': message.type}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllPersonalMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userID = User.objects.filter(username=username).first().id
        messageList = Message.objects.filter(receiverID=userID, type=2).order_by('-sendTime')
        ans_list = []
        for message in messageList:
            user = User.objects.filter(id=message.senderID).first()
            a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                 'content': message.content, 'postID': message.postID, 'viewed': message.viewed,
                 'type': message.type}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllReply(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userID = User.objects.filter(username=username).first().id
        messageList = Message.objects.filter(receiverID=userID, type=2).order_by('-sendTime')
        ans_list = []
        for message in messageList:
            user = User.objects.filter(id=message.senderID).first()
            a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                 'content': message.content, 'postID': message.postID, 'viewed': message.viewed,
                 'type': message.type}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllNotice(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userID = User.objects.filter(username=username).first().id
        messageList = Message.objects.filter(receiverID=userID, type=1).order_by('-sendTime')
        ans_list = []
        for message in messageList:
            user = User.objects.filter(id=message.senderID).first()
            a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                 'content': message.content, 'postID': message.postID, 'viewed': message.viewed,
                 'type': message.type}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showUnreadMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userID = User.objects.filter(username=username).first().id
        messageList = Message.objects.filter(receiverID=userID, viewed=False).order_by('-sendTime')
        ans_list = []
        for message in messageList:
            user = User.objects.filter(id=message.senderID).first()
            a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                 'content': message.content, 'postID': message.postID, 'viewed': message.viewed,
                 'type': message.type}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def deleteMessage(request):
    if request.method == 'POST':
        messageID = request.POST.get('messageID')
        existMessage = Message.objects.filter(id=messageID).first()
        if not existMessage:
            return JsonResponse({'status_code': 2, 'message': '不存在的消息!'})
        existMessage.delete()
        return JsonResponse({'status_code': 1, 'message': '删除成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})
from django.shortcuts import render

# Create your views here.
from .models import *
from users.models import User
import datetime
from interact.models import CommentOnPost, CommentOnLiterature
from post.models import Post


@csrf_exempt
def sendNotice(request):
    if request.method == 'POST':

        receiverName = request.POST.get('receiver')
        receiver = User.objects.filter(username=receiverName).first()
        message = request.POST.get('message')
        if message == None:
            return JsonResponse({'status_code': 2, 'message': '请输入通知内容!'})
        if receiver == None:
            return JsonResponse({'status_code': 3, 'message': '发送通知的对象不存在!'})

        newMessage = Message()
        newMessage.senderID = 0
        newMessage.content = message
        newMessage.receiverID = receiver.id
        newMessage.type = 1
        newMessage.sendTime = datetime.datetime.now()
        newMessage.save()

        return JsonResponse({'status_code': 1, 'message': '通知发送成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def sendPersonalMessage(request):
    if request.method == 'POST':
        senderName = request.POST.get('sender')
        receiverName = request.POST.get('receiver')
        sender = User.objects.filter(username=senderName).first()
        receiver = User.objects.filter(username=receiverName).first()
        message = request.POST.get('message')
        if message == None:
            return JsonResponse({'status_code': 2, 'message': '请输入私信内容!'})
        if receiver == None:
            return JsonResponse({'status_code': 3, 'message': '发送私信的对象不存在!'})

        newMessage = Message()
        newMessage.content = message
        newMessage.senderID = sender.id
        newMessage.receiverID = receiver.id
        newMessage.sendTime = datetime.datetime.now()
        newMessage.type = 2
        newMessage.save()
        return JsonResponse({'status_code': 1, 'message': '私信发送成功喵!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def sendReplyInPost(request):
    if request.method == 'POST':
        senderName = request.POST.get('sender')
        receiverName = request.POST.get('receiver')
        postID = request.POST.get('postID')
        floor = request.POST.get('floor')
        sender = User.objects.filter(username=senderName).first()
        receiver = User.objects.filter(username=receiverName).first()
        post = Post.objects.filter(id=postID).first()
        message = request.POST.get('message')
        if message == None:
            return JsonResponse({'status_code': 2, 'message': '请输入回复内容!'})
        if receiver == None:
            return JsonResponse({'status_code': 3, 'message': '发送回复的对象不存在!'})
        # 给动态发表评论
        newComment = CommentOnPost()
        newComment.content = message
        newComment.postID = postID
        newComment.floor = post.floors + 1
        newComment.commentTime = datetime.datetime.now()
        newComment.userID = sender.id
        post.floors += 1
        post.save()
        newComment.save()

        # 给被回复人发消息
        newMessage = Message()
        newMessage.content = message
        newMessage.senderID = sender.id
        newMessage.receiverID = receiver.id
        newMessage.postID = postID
        newMessage.sendTime = datetime.datetime.now()
        newMessage.type = 3
        newMessage.save()
        return JsonResponse({'status_code': 1, 'message': '回复发送成功喵!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


# @csrf_exempt
# def sendReplyInLiterature(request):
#     if request.method == 'POST':
#         senderName = request.POST.get('sender')
#         receiverName = request.POST.get('receiver')
#         literatureID = request.POST.get('literatureID')
#         floor = request.POST.get('floor')
#         sender = User.objects.get(username=senderName)
#         receiver = User.objects.get(username=receiverName)
#         literature = Literature.objects.get(id=literatureID)
#         message = request.POST.get('message')
#         if message == None:
#             return JsonResponse({'status_code': 2, 'message': '请输入回复内容!'})
#         if receiver == None:
#             return JsonResponse({'status_code': 3, 'message': '发送回复的对象不存在!'})
#         # 给动态发表评论
#         newComment = CommentOnLiterature()
#         newComment.content = message
#         newComment.literatureID = literatureID
#         newComment.floor = literature.floors + 1
#         newComment.commentTime = datetime.datetime.now()
#         newComment.userID = sender.id
#         literature.floors += 1
#         literature.save()
#         newComment.save()
#
#         # 给被回复人发消息
#         newMessage = Message()
#         newMessage.content = message
#         newMessage.senderID = sender.id
#         newMessage.receiverID = receiver.id
#         newMessage.postID = postID
#         newMessage.sendTime = datetime.datetime.now()
#         newMessage.type = 3
#         newMessage.save()
#         return JsonResponse({'status_code': 1, 'message': '回复发送成功喵!'})
#     return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

@csrf_exempt
def viewMessage(request):
    if request.method == 'POST':
        messageID = request.POST.get('messageID')
        message = Message.objects.filter(id=messageID).first()
        message.viewed = True
        message.save()
        return JsonResponse({'status_code': 1, 'message': '消息已读'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userID = User.objects.filter(username=username).first().id
        messageList = Message.objects.filter(receiverID=userID).order_by('-sendTime')
        ans_list = []
        for message in messageList:
            user = User.objects.filter(id=message.senderID).first()
            a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                 'content': message.content, 'postID': message.postID,
                 'type': message.type}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllPersonalMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        ans_list = []
        if User.objects.filter(username=username):
            userID = User.objects.filter(username=username).first().id
            messageList = Message.objects.filter(receiverID=userID, type=2).order_by('-sendTime')
            for message in messageList:
                user = User.objects.filter(id=message.senderID).first()
                a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                    'content': message.content, 'postID': message.postID,
                    'type': message.type}
                ans_list.append(a)
            return JsonResponse({'status_code': 1, 'ans_list': ans_list})
        else:
            return JsonResponse({'status_code': 1, 'ans_list': ans_list, 'msg':"没查询到该用户"})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllReply(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        ans_list = []
        if User.objects.filter(username=username):
            userID = User.objects.filter(username=username).first().id
            messageList = Message.objects.filter(receiverID=userID, type=3).order_by('-sendTime')
            for message in messageList:
                user = User.objects.filter(id=message.senderID).first()
                a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                    'content': message.content, 'postID': message.postID,
                    'type': message.type}
                ans_list.append(a)
            return JsonResponse({'status_code': 1, 'ans_list': ans_list})
        else:
            return JsonResponse({'status_code': 1, 'ans_list': ans_list, 'msg':"没查询到该用户"})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

@csrf_exempt
def showAllNotice(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        ans_list = []
        if User.objects.filter(username=username):
            userID = User.objects.filter(username=username).first().id
            messageList = Message.objects.filter(receiverID=userID, type=1).order_by('-sendTime')
            for message in messageList:
                user = User.objects.filter(id=message.senderID).first()
                a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                    'content': message.content, 'postID': message.postID,
                    'type': message.type}
                ans_list.append(a)
            return JsonResponse({'status_code': 1, 'ans_list': ans_list})
        else:
            return JsonResponse({'status_code': 1, 'ans_list': ans_list, 'msg':"没查询到该用户"})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

@csrf_exempt
def showUnreadMessage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userID = User.objects.filter(username=username).first().id
        messageList = Message.objects.filter(receiverID=userID, viewed=False).order_by('-sendTime')
        ans_list = []
        for message in messageList:
            user = User.objects.filter(id=message.senderID).first()
            a = {'messageID': message.id, 'userID': user.id, 'sender': user.username, 'avatar': user.avatar,
                 'content': message.content, 'postID': message.postID,
                 'type': message.type}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def deleteMessage(request):
    if request.method == 'POST':
        messageID = request.POST.get('messageID')
        existMessage = Message.objects.filter(id=messageID).first()
        if not existMessage:
            return JsonResponse({'status_code': 2, 'message': '不存在的消息!'})
        existMessage.delete()
        return JsonResponse({'status_code': 1, 'message': '删除成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})
