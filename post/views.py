from django.shortcuts import render
import json
import re
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from .models import *
from post.models import Post
from sector.models import Sector
from users.models import User
from interact.models import CommentOnPost
from interact.models import CommentOnLiterature
from sector.models import Sector



@csrf_exempt
def getOnesPost(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        posts = Post.objects.filter(posterID=user.id)
        ans_list = []
        for post in posts:
            a = {
                'id': post.id,
                'sectorID': post.sectorID,
                'postContent': post.postContent,
                'postTime': post.postTime,
                'referenceDocID': post.referenceDocID,
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def post(request):
    if request.method == 'POST':
        referenceDocID = request.POST.get('articleID')
        postContent = request.POST.get('content')
        posterID = request.POST.get('posterID')
        sectorID = request.POST.get('sectorID')
        tags = request.POST.get('tags')
        try:
            sector = Sector.objects.get(id=sectorID)
            sector.counter = sector.counter + 1
            sector.save()
        except:
            return JsonResponse({'status_code': 2, 'msg': '对应分区不存在'})
        post = Post()
        post.referenceDocID = referenceDocID
        post.postContent = postContent
        post.posterID = posterID
        post.sectorID = sectorID
        post.tags = tags
        post.save()
        return JsonResponse({'status_code': 1, 'msg': '发布动态成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def canclePost(request):
    if request.method == 'POST':
        postID = request.POST.get('postID')
        try:
            post = Post.objects.get(id=postID)
            try:
                sector = Sector.objects.get(id=post.sectorID)
                sector.counter = sector.counter - 1
                sector.save()
            except:
                None
            post.delete()
            comments = CommentOnPost.objects.filter(postID=postID)
            for comment in comments:
                comment.delete()
            return JsonResponse({'status_code': 1, 'msg': '删除动态成功'})
        except:
            return JsonResponse({'status_code': 2, 'msg': '该动态不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def getPostComment(request):
    if request.method == 'POST':
        postID = request.POST.get('postID')
        try:
            post = Post.objects.get(id=postID)
        except:
            return JsonResponse({'status_code': 2, 'msg': '该动态不存在'})
        comments = CommentOnPost.objects.filter(postID=postID)
        comment_list = []
        for comment in comments:
            dict = {
                "username": User.objects.filter(id=comment.userID).first().username,
                'avatar': User.objects.filter(id=comment.userID).first().avatar,
                "content": comment.content,
                "commentTime": comment.commentTime,
                "floor": comment.floor
            }
            comment_list.append(dict)
        return JsonResponse({'status_code': 1, 'comments': comment_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


# 将对论文的评论转为动态
@csrf_exempt
def commentToPost(request):
    if request.method == 'POST':
        commentID = request.POST.get('commentID')
        username = request.POST.get('username')
        sectorID = request.POST.get('sectorID')
        tags = request.POST.get('tags')
        try:
            sector = Sector.objects.get(id=sectorID)
            sector.counter = sector.counter + 1
            sector.save()
        except:
            return JsonResponse({'status_code': 4, 'msg': '对应分区不存在'})
        try:
            comment = CommentOnLiterature.objects.get(id=commentID)
            existPost = Post.objects.filter(referenceDocID=comment.literatureID, postContent=comment.content,
                                           posterID=comment.userID)
            if existPost:
                return JsonResponse({'status_code': 3, 'msg': '已存在相关动态'})
            post = Post()
            post.referenceDocID = comment.literatureID
            post.postContent = "//@" + User.objects.filter(id=comment.userID).first().username + ":" + comment.content
            post.posterID = User.objects.filter(username=username).first().id
            post.sectorID = sectorID
            post.tags = tags
            post.save()
            sector = Sector.objects.filter(id=sectorID).first()
            sector.counter += 1
            sector.save()
            return JsonResponse({'status_code': 1, 'msg': '发布动态成功'})
        except:
            return JsonResponse({'status_code': 2, 'msg': '该评论不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


# 获取动态所有信息，包括评论
@csrf_exempt
def getPostInfo(request):
    if request.method == 'POST':
        postID = request.POST.get('postID')
        try:
            post = Post.objects.get(id=postID)
            comments = CommentOnPost.objects.filter(postID=postID)
            comment_list = []
            for comment in comments:
                dict = {
                    "userID": comment.userID,
                    "content": comment.content,
                    "commentTime": comment.commentTime,
                    "floor": comment.floor
                }
                comment_list.append(dict)
            return JsonResponse({
                'status_code': 1,
                'referenceDocID': post.referenceDocID,
                'postContent': post.postContent,
                'posterID': post.posterID,
                'postTime': post.postTime,
                'tags': post.tags,
                'floors': post.floors,
                'sectorID': post.sectorID,
                'comments': comment_list
            })
        except:
            return JsonResponse({'status_code': 2, 'msg': '该动态不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})

@csrf_exempt
def passPost(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        postID = request.POST.get('postID')
        content = request.POST.get('content')
        try:
            post = Post.objects.get(id=postID)
            try:
                user=User.objects.get(username=username)
                new_post=Post()
                new_post.posterID=user.id
                new_post.postContent=content
                new_post.referenceDocID=post.referenceDocID
                new_post.tags=post.tags
                new_post.sectorID = post.sectorID
                new_post.save()
                return JsonResponse({'status_code': 1, 'msg': '转发成功'})
            except:
                return JsonResponse({'status_code': 3, 'msg': '该用户不存在'})
        except:
            return JsonResponse({'status_code': 2, 'msg': '该动态不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})