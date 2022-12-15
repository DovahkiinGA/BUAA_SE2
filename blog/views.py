# # Create your views here.
# import json
# import re
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from pytz import utc
# import requests
# from users.models import User
# from utils.email import *
# from utils.token import create_token
# from utils.token import check_token
# from .models import *
# from .search_views import MySeachView
# from blog import forms
# from haystack.views import basic_search
# @csrf_exempt
# def search(request):
#     if request.method == 'GET':
#         print("=====================im in views.py")
#         sv=MySeachView(form_class=forms.keywordSearch)
#         return sv(request)
