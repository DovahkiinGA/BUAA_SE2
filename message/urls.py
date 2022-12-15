from django.urls import path
from .views import *

urlpatterns = [
    path('sendPersonalMessage', sendPersonalMessage),
    path('showAllMessage', showAllMessage),
    path('showUnreadMessage', showUnreadMessage),
    path('viewMessage', viewMessage),
    path('deleteMessage', deleteMessage),
    path('showAllPersonalMessage', showAllPersonalMessage),
    path('showAllReply', showAllReply),
    path('showAllNotice', showAllNotice),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
    # path('showMessage', showMessage),
]
