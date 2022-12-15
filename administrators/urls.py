from django.urls import path
from .views import *
urlpatterns = [
    path('register', register),
    path('get_info', get_info),
    path('solve_report', solve_report),

    path('showApplication', showApplication),
    path('acceptApplication', acceptApplication),
    path('refuseApplication', refuseApplication),
    # path('register', register),
    # path('register', register),
    # path('register', register),
    # path('register', register),
    # path('register', register),
]