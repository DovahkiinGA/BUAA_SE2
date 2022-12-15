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
from interact.models import CommentOnPost, CommentOnLiterature, FollowSector
from post.models import Post
from collections import Counter
from scholar_data.models import Papers
from django.db.models import QuerySet
from django.forms.models import model_to_dict

# Create your views here.

@csrf_exempt
def showAllSector(request):
    if request.method == 'POST':

        sectors = Sector.objects.all()
        ans_list = []
        for sector in sectors:
            a = {'name': sector.name, 'counter': sector.counter, 'id': sector.id}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showFollowingSector(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        follows = FollowSector.objects.filter(userID=user.id)
        ans_list = []
        for follow in follows:
            sector = Sector.objects.filter(id=follow.sectorID).first()
            a = {'name': sector.name, 'counter': sector.counter, 'id': sector.id}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def showAllSectorPlus(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.filter(username=username).first()
            sectors = Sector.objects.all()
            ans_list = []
            for sector in sectors:
                try:
                    follow = FollowSector.objects.get(userID=user.id, sectorID=sector.id)
                    a = {'name': sector.name, 'counter': sector.counter, 'id': sector.id, 'isFollow': 1}
                except:
                    a = {'name': sector.name, 'counter': sector.counter, 'id': sector.id, 'isFollow': 0}
                ans_list.append(a)
            return JsonResponse({'status_code': 1, 'ans_list': ans_list})
        except:
            return JsonResponse({'status_code': 2, 'msg': '该用户不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def followSector(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        sectorName = request.POST.get('sectorName')
        try:
            user = User.objects.get(username=username)
            try:
                sector = Sector.object.get(name=sectorName)
                try:
                    follow = FollowSector.objects.get(userID=user.id, sectorID=sector.id)
                    return JsonResponse({'status_code': 4, 'msg': '用户已关注该分区'})
                except:
                    follow = FollowSector()
                    follow.userID = user.id
                    follow.sectorID = sector.id
                    follow.save()
                    return JsonResponse({'status_code': 1, 'msg': '关注分区成功'})
            except:
                return JsonResponse({'status_code': 3, 'msg': '该分区不存在'})
        except:
            return JsonResponse({'status_code': 2, 'msg': '该用户不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def unfollowSector(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        sectorName = request.POST.get('sectorName')
        try:
            user = User.objects.get(username=username)
            try:
                sector = Sector.object.get(name=sectorName)
                try:
                    follow = FollowSector.objects.get(userID=user.id, sectorID=sector.id)
                    follow.delete()
                    return JsonResponse({'status_code': 1, 'msg': '取消关注分区成功'})
                except:
                    return JsonResponse({'status_code': 4, 'msg': '用户未关注该分区'})
            except:
                return JsonResponse({'status_code': 3, 'msg': '该分区不存在'})
        except:
            return JsonResponse({'status_code': 2, 'msg': '该用户不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})


@csrf_exempt
def getSectorPost(request):
    if request.method == 'POST':
        sectorName = request.POST.get('sectorName')
        try:
            sector = Sector.object.get(name=sectorName)
            posts = Post.objects.filter(sectorID=sector.id)
            post_list = []
            docID_list = []
            for post in posts:
                docID_list.append(post.referenceDocID)
                dict = {
                    'referenceDocID': post.referenceDocID,
                    'postContent': post.postContent,
                    'posterID': post.posterID,
                    'postTime': post.postTime,
                    'tags': post.tags,
                    'floors': post.floors
                }
                post_list.append(dict)
            number = Counter(docID_list)
            hot = number.most_common()
            hot_docs = []
            for i in range(0, 3, 1):
                if i == len(hot):
                    break
                dict = {
                    'docID': hot[i][0],
                    'hot': hot[i][1]
                }
                hot_docs.append(dict)
            i = 3
            while i < len(hot) and hot[i][1] == hot[2][1]:
                dict = {
                    'docID': hot[i][0],
                    'hot': hot[i][1]
                }
                hot_docs.append(dict)
                i = i + 1
            return JsonResponse({'status_code': 1, 'posts': post_list, 'hot_docs': hot_docs})
        except:
            return JsonResponse({'status_code': 2, 'msg': '该分区不存在'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

@classmethod
def compare_posts_by_time(post1, post2):
    if post1.postTime < post2.postTime:
        return -1
    elif post1.postTime > post2.postTime:
        return 1
    else:
        return 0


@csrf_exempt
def getPostsInSector(request):
    if request.method == 'POST':
        sectors = request.POST.get('sectors')
        print("----------")
        print(sectors)
        print("----------")
        sectors=sectors.split('|')
        start = request.POST.get('start')
        num = request.POST.get('num')
        if num is None or num=="":
            num=10
        ans_list = []
        post_list = []
        docID_list=[]
        for sectorName in sectors:
            try:
                sector = Sector.objects.filter(name=sectorName).first()
                posts=Post.objects.filter(sectorID=sector.id)
                for post in posts:
                    post_list.append(post)
            except:
                print("error")
        for post in post_list:
            docID_list.append(post.referenceDocID)

        for post in post_list[int(start):int(start)+int(num)]:
            user=User.objects.filter(id=post.posterID).first()
            a = {
                'sectorID': post.sectorID, 'postID': post.id, 'postContent': post.postContent,
                'postTime': post.postTime, 'referenceDocID': post.referenceDocID,'username':user.username,
                'avatar': user.avatar
            }
            ans_list.append(a)
        number = Counter(docID_list)
        hot = number.most_common()
        hot_docs = []
        for i in range(0, 3, 1):
            if i == len(hot):
                break
            paper=Papers.objects.filter(id=hot[i][0]).first()
            dict = {
                'id': paper.id,
                'title': paper.title,
                'keywords': paper.keywords
            }
            hot_docs.append(dict)
        return JsonResponse({'status_code': 1, 'posts': ans_list, 'docs': hot_docs})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误!'})

