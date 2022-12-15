from django.shortcuts import render
import json
import re
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from .models import *
from users.models import User
from interact.models import CommentOnLiterature
# Create your views here

@csrf_exempt
def viewPaper(request):
    if request.method == 'POST':
        paperID = request.POST.get('paperID')
        # todo:查找到那个paper
        paper = Papers.objects.filter(id=paperID).first()
        print("paper----------------------------------")
        print(paper.id)
        print(paper.title)
        ans = {
            'id': paperID,
            'title': paper.title,
            'auth': eval(paper.auth),
            'lang': paper.lang,
            'issn': paper.issn,
            'isbn': paper.isbn,
            'doi': paper.doi,
            'pdf': paper.pdf,
            'url': eval(paper.url),
            'abstract': paper.abstract,
            'year': paper.year,
            'doc_type': paper.doc_type,
            'n_citation': paper.n_citation,
            'keywords': eval(paper.keywords)
        }
        return JsonResponse({'status_code': 1, 'ans': ans})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def viewCommentOnPaper(request):
    if request.method == 'POST':
        paperID = request.POST.get('paperID')

        comments = CommentOnLiterature.objects.filter(literatureID=paperID)
        ans_list = []
        for comment in comments:
            user = User.objects.filter(id=comment.userID).first()
            a = {
                'id': comment.id,
                'content': comment.content,
                'username': user.username,
                'avatar': user.avatar,
                'commentTime': comment.commentTime,
                'floor': comment.floor,
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def searchAuthor(request):
    if request.method == 'POST':
        authName = request.POST.get('authName')
        auths = Authors.objects.filter(name__icontains=authName)
        ans_list = []
        for auth in auths:
            a = {
                'authorName': auth.name,
                'authorId': auth.id
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'length': len(ans_list), 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})


@csrf_exempt
def searchAuthPubs(request):
    if request.method == 'POST':
        authId = request.POST.get('authId')
        auth = Authors.objects.filter(id=authId).first()
        pubs = eval(auth.pubs)
        n_pubs = len(pubs)
        pub_list = []  # 文章id
        for i in range(n_pubs):
            pub_list.append(pubs[i]["i"])
        ans_list = []
        i=0
        for pub_id in pub_list:
            paper = Papers.objects.filter(id=pub_id).first()
            if paper == None:
                continue
            a = {
                'id': pub_id,
                'title': paper.title,
                'auth': getPaperAuthName(paper.auth),
                'year': paper.year,
                'doc_type': paper.doc_type,
                'n_citation': paper.n_citation,
                'keywords': eval(paper.keywords)
            }
            i+=1
            if i>3:
                break
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'length': len(ans_list), 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})

@csrf_exempt
def searchAuthAllPubs(request):
    print("--------------------------------------------------------------------")
    if request.method == 'POST':
        authId = request.POST.get('authId')
        auth = Authors.objects.filter(id=authId).first()
        pubs = eval(auth.pubs)
        n_pubs = len(pubs)
        pub_list = []  # 文章id
        for i in range(n_pubs):
            pub_list.append(pubs[i]["i"])
        ans_list = []
        for pub_id in pub_list:
            paper = Papers.objects.filter(id=pub_id).first()
            if paper == None:
                continue
            #paper = Papers.objects.get(id=pub_id)
            a = {
                'id': pub_id,
                'title': paper.title,
                'auth': getPaperAuthName(paper.auth),
                'year': paper.year,
                'doc_type': paper.doc_type,
                'n_citation': paper.n_citation,
                'keywords': eval(paper.keywords)
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'length': len(ans_list), 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})

@csrf_exempt
def searchAuthAllPubs(request):
    if request.method == 'POST':
        authId = request.POST.get('authId')
        auth = Authors.objects.filter(id=authId).first()
        pubs = eval(auth.pubs)
        n_pubs = len(pubs)
        pub_list = []  # 文章id
        for i in range(n_pubs):
            pub_list.append(pubs[i]["i"])
        ans_list = []
        for pub_id in pub_list:
            paper = Papers.objects.filter(id=pub_id).first()
            a = {
                'id': pub_id,
                'title': paper.title,
                'auth': getPaperAuthName(paper.auth),
                'year': paper.year,
                'doc_type': paper.doc_type,
                'n_citation': paper.n_citation,
                'keywords': eval(paper.keywords)
            }
            ans_list.append(a)
        return JsonResponse({'status_code': 1, 'length': len(ans_list), 'ans_list': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})

def getPaperAuthName(text):
    text = eval(text)
    name_list = []
    if not isinstance(text, list):
        return name_list
    else:
        if len(text) == 0:
            return name_list
    for auth in text:
        name = auth["name"]
        name_list.append(name)
    return name_list

@csrf_exempt
def getOverview(request):
    if request.method == 'POST':
        new_data = DownloadandSearch.objects.all().order_by("-id")[:7]
        ans_list = []
        for data in new_data:
            a = {
                'search': data.search,
                'download': data.download,
            }
            ans_list.append(a)
        return JsonResponse({'status_code':0, 'data': ans_list})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})

