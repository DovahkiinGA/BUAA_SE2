from django.urls import path
from .views import *

urlpatterns = [
    path('post', post),
    path('canclePost', canclePost),
    path('getPostComment', getPostComment),
    path('commentToPost', commentToPost),
    path('getPostInfo', getPostInfo),
    path('getOnesPost', getOnesPost),
    path('passPost', passPost),
    path('commentToPost', commentToPost),
    # path('getPostInfo', getPostInfo),
    # path('getPostComment', getPostComment),
    # path('commentToPost', commentToPost),
    # path('getPostInfo', getPostInfo),
]

