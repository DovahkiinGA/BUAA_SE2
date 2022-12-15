from django.urls import path
from .views import *
urlpatterns = [
    path('showAllSector', showAllSector),
    path('showFollowingSector', showFollowingSector),
    path('followSector', followSector),
    path('unfollowSector', unfollowSector),
    path('getSectorPost', getSectorPost),
    path('showAllSectorPlus', showAllSectorPlus),
    path('getPostsInSector', getPostsInSector),

    # path('showAllSector', showAllSector),
    # path('showAllSector', showAllSector),
    # path('showAllSector', showAllSector),
    # path('showAllSector', showAllSector),
    # path('showAllSector', showAllSector),
    # path('showAllSector', showAllSector),
    # path('showAllSector', showAllSector),
]
