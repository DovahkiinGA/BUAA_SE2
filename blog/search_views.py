# 重写SearchView，实现自定义内容
# blog/search_views.py
from haystack.views import SearchView

# 导入模块
from .models import *
from django.http import JsonResponse
from .forms import keywordSearch

class MySeachView(SearchView):
    # form_class=keywordSearch
    form_class=keywordSearch

    def create_response(self):
        print("=====================im in response")
        print(self.request)
        context = self.get_context()
        data_list=[]
        for i in context['page'].object_list:
            data_dict={}
            data_dict['title']=i.object.title
            data_dict['topic']=i.object.topic
            data_dict['content']=i.object.content
            data_dict['auth']=i.object.auth
            data_dict['asso']=i.object.asso
            data_dict['jour']=i.object.jour
            data_dict['date']=i.object.date
            data_list.append(data_dict)
        print(len(data_list))
        print(data_list)
        return JsonResponse(data_list,safe=False)
