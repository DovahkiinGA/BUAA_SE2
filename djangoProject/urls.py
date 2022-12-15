"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path

from djangoProject import settings


from rest_framework import routers
# from blog import search_views
# from blog import forms
from scholar_data import search_views
from scholar_data import forms
router = routers.DefaultRouter()

urlpatterns = [
 
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/administrators/', include('administrators.urls')),
    path('api/sector/', include('sector.urls')),
    path('api/message/', include('message.urls')),
    path('api/post/', include('post.urls')),
    path('api/interact/', include('interact.urls')),
    path('api/scholar_data/', include('scholar_data.urls')),
    # path('api/search/', include(('blog.urls'))),
   
    #re_path(r'^search/', include('haystack.urls')),
    path('api/search/scholarsearch/', search_views.MyScholarSeachView(
        form_class=forms.ScholarkeywordSearch
    ), name='haystack_search'),
    path('api/search/suggestion/', search_views.MySuggestSeachView(
        form_class=forms.ScholarSuggestSearch
    ), name='haystack_search'),
    path('api/search/morelikethis/', search_views.MorelikethisSeachView(
        form_class=forms.MorelikethisSearch
    ), name='haystack_search'),
]

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

