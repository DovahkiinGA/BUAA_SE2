from django.urls import path
from .views import *

urlpatterns = [

    path('viewPaper', viewPaper),
    path('viewCommentOnPaper', viewCommentOnPaper),
    path('searchAuthor',searchAuthor),
    path('searchAuthPubs',searchAuthPubs),
    path('searchAuthAllPubs', searchAuthAllPubs),
    path('getOverview',getOverview)

    # path('getPostComment', getPostComment),
    # path('commentToPost', commentToPost),
    # path('getPostInfo', getPostInfo),
    # path('getOnesPost', getOnesPost),
    # path('passPost', passPost),
    # path('commentToPost', commentToPost),
    # path('getPostInfo', getPostInfo),
    # path('getPostComment', getPostComment),
    # path('commentToPost', commentToPost),
    # path('getPostInfo', getPostInfo),
]
