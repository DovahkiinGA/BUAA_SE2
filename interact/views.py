from django.shortcuts import render
import json
import re
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from .models import *
from users.models import User
from sector.models import Sector
from post.models import Post
from scholar_data.models import Papers


# Create your views here.

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        followerUsername = request.POST.get('follower')
        followeeUsername = request.POST.get('followee')
        followerID = User.objects.filter(username=followerUsername).first().id
        followeeID = User.objects.filter(username=followeeUsername).first().id
        existFollower = Follow.objects.filter(followeeID=followeeID, followerID=followerID)
        if existFollower:
            return JsonResponse({'status_code': 2, 'msg': '已关注该用户，请勿重复关注'})
        else:
            newFollow = Follow()
            newFollow.followerID = followerID
            newFollow.followeeID = followeeID
            newFollow.followTime = datetime.datetime.now()
            newFollow.save()
            return JsonResponse({'status_code': 1, 'msg': '关注成功喵'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def cancelFollow(request):
    if request.method == 'POST':
        followerUsername = request.POST.get('follower')
        followeeUsername = request.POST.get('followee')
        followerID = User.objects.filter(username=followerUsername).first().id
        followeeID = User.objects.filter(username=followeeUsername).first().id

        existFollower = Follow.objects.filter(followeeID=followeeID, followerID=followerID)
        if not existFollower:
            return JsonResponse({'status_code': 2, 'msg': '该用户未关注该用户，取消关注失败'})
        else:
            existFollower.delete()
            return JsonResponse({'status_code': 1, 'msg': '取消关注成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def getFollow(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        thisUser = User.objects.filter(username=username).first()
        follows = Follow.objects.filter(followerID=thisUser.id).order_by('-followTime')

        ans_list = []
        for follow in follows:
            followee = User.objects.filter(id=follow.followeeID).first()
            a = {'username': followee.username, 'avatar': followee.avatar, 'followTime': follow.followTime,
                 'brief_intro': followee.brief_intro}
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def queryFollow(request):
    if request.method == 'POST':
        followerUsername = request.POST.get('follower')
        followeeUsername = request.POST.get('followee')
        followerID = User.objects.filter(username=followerUsername).first().id
        followeeID = User.objects.filter(username=followeeUsername).first().id
        existFollower = Follow.objects.filter(followeeID=followeeID, followerID=followerID)
        if existFollower:
            return JsonResponse({'status_code': 1, 'msg': '已关注'})
        else:

            return JsonResponse({'status_code': 2, 'msg': '未关注'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def followSector(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        sectorName = request.POST.get('sectorName')
        userID = User.objects.filter(username=username).first().id
        sectorID = Sector.objects.filter(name=sectorName).first().id
        existFollowSector = FollowSector.objects.filter(userID=userID, sectorID=sectorID)
        if existFollowSector:
            return JsonResponse({'status_code': 2, 'msg': '已关注该分区，请勿重复关注'})
        else:
            newFollow = FollowSector()
            newFollow.userID = userID
            newFollow.sectorID = sectorID
            newFollow.followTime = datetime.datetime.now()
            newFollow.save()
            return JsonResponse({'status_code': 1, 'msg': '关注成功喵'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def unfollowSector(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        sectorName = request.POST.get('sectorName')
        userID = User.objects.filter(username=username).first().id
        sectorID = Sector.objects.filter(name=sectorName).first().id
        existFollowSector = FollowSector.objects.filter(userID=userID, sectorID=sectorID)
        if existFollowSector:
            existFollowSector.delete()
            return JsonResponse({'status_code': 1, 'msg': '取消关注成功'})
        else:
            return JsonResponse({'status_code': 2, 'msg': '未关注哈'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def collect(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        literatureID = request.POST.get('literatureID')
        # todo:验证是否有这个文献
        # collect success
        userID = User.objects.get(username=username).id
        new_collection = Collection()
        new_collection.userID = userID
        new_collection.literatureID = literatureID
        new_collection.collectTime = datetime.datetime.now()
        new_collection.save()
        return JsonResponse({'status_code': 1, 'msg': '收藏成功'})
    else:
        return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def cancelCollect(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        literatureID = request.POST.get('literatureID')
        userID = User.objects.get(username=username).id
        existCollection = Collection.objects.filter(userID=userID, literatureID=literatureID)
        if not existCollection:
            return JsonResponse({'status_code': 2, 'msg': '该用户未收藏该文献，取消收藏失败'})
        else:
            Collection.objects.filter(userID=userID, literatureID=literatureID).first().delete()
            return JsonResponse({'status_code': 1, 'msg': '取消收藏成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def getCollections(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        ans_list = []
        collections = Collection.objects.filter(userID=User.objects.filter(username=username).first().id)
        for collection in collections:
            paper=Papers.objects.filter(id=collection.literatureID).first()
            a = {
                'literatureID': collection.literatureID,
                'collectTime': collection.collectTime,
                'title':paper.title,
                'lang':paper.lang
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})

    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def reportArticle(request):
    if request.method == 'POST':
        reporterUsername = request.POST.get('reporter')
        reporteeUsername = request.POST.get('reportee')
        objectID = request.POST.get('articleID')
        content = request.POST.get('content')
        reporterID = User.objects.filter(username=reporterUsername).first().id
        reporteeID = User.objects.filter(username=reporteeUsername).first().id
        existReporter = Report.objects.filter(reporterID=reporterID, reporteeID=reporteeID, type=1,
                                              objectID=objectID,
                                              result=None)
        if existReporter:
            return JsonResponse({'status_code': 2, 'msg': '已经存在相关举报了'})
        else:
            newReport = Report()
            newReport.reporterID = reporterID
            newReport.reporteeID = reporteeID
            newReport.objectID = objectID
            newReport.type = 1
            newReport.content = content
            newReport.reportTime = datetime.datetime.now()
            newReport.result = 0
            newReport.save()
            return JsonResponse({'status_code': 1, 'msg': '举报成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def reportComment(request):
    if request.method == 'POST':
        reporterUsername = request.POST.get('reporter')
        reporteeUsername = request.POST.get('reportee')
        objectID = request.POST.get('commentID')
        content = request.POST.get('content')
        reporterID = User.objects.filter(username=reporterUsername).first().id
        reporteeID = User.objects.filter(username=reporteeUsername).first().id
        existReporter = Report.objects.filter(reporterID=reporterID, reporteeID=reporteeID, type=2,
                                              objectID=objectID,
                                              result=None)
        if existReporter:
            return JsonResponse({'status_code': 2, 'msg': '已经存在相关举报了'})
        else:
            newReport = Report()
            newReport.reporterID = reporterID
            newReport.reporteeID = reporteeID
            newReport.objectID = objectID
            newReport.type = 2
            newReport.content = content
            newReport.reportTime = datetime.datetime.now()
            newReport.result = 0
            newReport.save()
            return JsonResponse({'status_code': 1, 'msg': '举报成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def reportPost(request):
    if request.method == 'POST':
        reporterUsername = request.POST.get('reporter')
        reporteeUsername = request.POST.get('reportee')
        objectID = request.POST.get('postID')
        content = request.POST.get('content')
        reporterID = User.objects.filter(username=reporterUsername).first().id
        reporteeID = User.objects.filter(username=reporteeUsername).first().id
        existReporter = Report.objects.filter(reporterID=reporterID, reporteeID=reporteeID, type=3,
                                              objectID=objectID,
                                              result=None)
        if existReporter:
            return JsonResponse({'status_code': 2, 'msg': '已经存在相关举报了'})
        else:
            newReport = Report()
            newReport.reporterID = reporterID
            newReport.reporteeID = reporteeID
            newReport.objectID = objectID
            newReport.type = 3
            newReport.content = content
            newReport.reportTime = datetime.datetime.now()
            newReport.result = 0
            newReport.save()
            return JsonResponse({'status_code': 1, 'msg': '举报成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def reportAuthor(request):
    if request.method == 'POST':
        reporterUsername = request.POST.get('reporter')
        reporteeUsername = request.POST.get('reportee')
        objectID = request.POST.get('authorID')
        content = request.POST.get('content')
        reporterID = User.objects.filter(username=reporterUsername).first().id
        reporteeID = User.objects.filter(username=reporteeUsername).first().id
        existReporter = Report.objects.filter(reporterID=reporterID, reporteeID=reporteeID, type=4,
                                              objectID=objectID,
                                              result=None)
        if existReporter:
            return JsonResponse({'status_code': 2, 'msg': '已经存在相关举报了'})
        else:
            newReport = Report()
            newReport.reporterID = reporterID
            newReport.reporteeID = reporteeID
            newReport.objectID = objectID
            newReport.type = 4
            newReport.content = content
            newReport.reportTime = datetime.datetime.now()
            newReport.result = 0
            newReport.save()
            return JsonResponse({'status_code': 1, 'msg': '举报成功'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def cancelReport(request):
    if request.method == 'POST':
        reportID = request.POST.get('reportID')
        try:
            report = Report.objects.get(id=reportID)

            if report.result != 0:
                return JsonResponse({'status_code': 2, 'msg': '该举报已被处理'})
            else:
                report.delete()
                return JsonResponse({'status_code': 1, 'msg': '取消举报成功'})
        except:
            return JsonResponse({'status_code': 3, 'msg': '该举报不存在'})

    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def commentOnPost(request):
    if request.method == 'POST':
        postID = request.POST.get('postID')
        content = request.POST.get('content')
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        userID = user.id
        post = Post.objects.filter(id=postID).first()

        newComment = CommentOnPost()
        newComment.postID = postID
        newComment.content = content
        newComment.userID = userID
        newComment.commentTime = datetime.datetime.now()
        newComment.floor = post.floors + 1
        post.floors += 1
        post.save()
        newComment.save()
        return JsonResponse({'status_code': 1, 'message': '评论成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def commentOnPaper(request):
    if request.method == 'POST':
        paperID = request.POST.get('paperID')
        content = request.POST.get('content')
        username = request.POST.get('username')
        needPost = request.POST.get('needPost')
        # 0 不转发,1转发
        user = User.objects.filter(username=username).first()
        userID = user.id
        print("userID")
        print(userID)
        paper = Papers.objects.filter(id=paperID).first()
        print("paperID")
        print(paperID)
        newComment = CommentOnLiterature()
        newComment.literatureID = paperID
        newComment.content = content
        newComment.userID = userID
        newComment.commentTime = datetime.datetime.now()
        newComment.save()
        print("before judge")
        if needPost == "1":
            print("postID")
            post = Post()
            post.referenceDocID = paperID
            post.postContent = content
            post.posterID = userID
            post.postTime = datetime.datetime.now()
            print(post.id)
            existSector = Sector.objects.filter(name=paper.title)
            if existSector:
                sector = Sector.objects.filter(name=paper.title).first()
                sector.counter += 1
                print("sectorID")
                # print(sector.id)
                sector.save()
                post.sectorID = sector.id
                post.save()
            else:
                newSector = Sector()
                newSector.name = paper.title
                newSector.counter = 1
                print("newSectorID")
                # print(newSector.id)

                newSector.save()
                post.sectorID = newSector.id
                post.save()
            # sectorID
        return JsonResponse({'status_code': 1, 'message': '评论成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def apply(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        authorID = request.POST.get('authorID')
        content = request.POST.get('content')

        apply = Apply()
        apply.userID = User.objects.filter(username=username).first().id
        apply.authorID = authorID
        apply.content = content
        apply.applyTime = datetime.datetime.now()
        apply.save()

        return JsonResponse({'status_code': 1, 'message': '申请门户成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})
