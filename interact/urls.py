from django.urls import path
from .views import *

urlpatterns = [
    path('collect', collect),
    path('cancelCollect', cancelCollect),
    path('follow', follow),
    path('cancelFollow', cancelFollow),
    path('queryFollow', queryFollow),
    path('reportArticle', reportArticle),
    path('reportComment', reportComment),
    path('reportPost', reportPost),
    path('reportAuthor', reportAuthor),
    path('cancelReport', cancelReport),
    path('getFollow', getFollow),
    path('followSector', followSector),
    path('unfollowSector', unfollowSector),
    path('commentOnPost', commentOnPost),
    path('getCollections', getCollections),
    path('apply', apply),
    path('commentOnPaper', commentOnPaper),
    # path('collect', collect),
    # path('collect', collect),
    # path('collect', collect),
    # path('collect', collect),
    # path('collect', collect),
    # path('collect', collect),
    # path('collect', collect),
]
