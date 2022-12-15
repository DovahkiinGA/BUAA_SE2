from django.urls import path
from .views import *
urlpatterns = [
    path('login', login),
    path('register', register),
    path('confirm/email', user_confirm),
    path('get_userinfo', get_userinfo),
    path('change_password', change_password),
    path('update/info', update_info),
    path('get_all', get_all),
    path('get_one', get_one),
]
