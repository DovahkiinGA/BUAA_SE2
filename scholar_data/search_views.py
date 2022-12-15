# 重写SearchView，实现自定义内容
# blog/search_views.py
from haystack.views import SearchView
import json
# 导入模块
from .models import *
# from .sbdata import imsb1
from django.http import JsonResponse
from .forms import ScholarkeywordSearch
# from .highlighter import myHighlighter
import math
from haystack.utils.highlighting import Highlighter
"""
自定义关键词高亮器，不截断过短的文本（例如文章标题）
"""
from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter

class myHighlighter(HaystackHighlighter):
    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        # if len(text_block) < self.max_length:
        if len(text_block) <3000:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)
class MyScholarSeachView(SearchView):
    # form_class=keywordSearch
    form_class=ScholarkeywordSearch
    
    def create_response(self):
        
        print("=====================im in response")

        q=self.request.GET.get("q")
        formula=json.loads(q)
        group=formula['group']
        hahatitle=""
        hahaabs=""
        for i in group:
            for j in i:
                if(j['kind']=='title'):
                    hahatitle=j['content']
                if(j['kind']=='abstract'):
                    hahaabs=j['content']
        context = self.get_context()
        print(len(self.results))
        # print(self.results)
        data_list=[]
        for i in context['page'].object_list:
            try:
                strkey=i.object.keywords
                strauth=i.object.auth
                if(strkey=="-1"):
                    strkey="[]"
                if(strauth=="-1"):
                    strauth="[]"
                highlight = myHighlighter(hahatitle)
                i.object.title=highlight.highlight(i.object.title)
                highlight = myHighlighter(hahaabs)
                i.object.abstract=highlight.highlight(i.object.abstract)
                arrkey =  eval('(' + strkey + ')')
                arrauth =  eval('(' + strauth + ')')
                data_dict={}            
                data_dict['title']=i.object.title
                data_dict['id']=i.object.id
                data_dict['auth']=arrauth
                data_dict['year']=i.object.year
                data_dict['keywords']=arrkey
                data_dict['fos']=i.object.fos
                data_dict['n_citation']=i.object.n_citation
                data_dict['publisher']=i.object.publisher
                data_dict['issue']=i.object.issue
                data_dict['abstract']=i.object.abstract
                data_dict['doi']=i.object.doi
                data_list.append(data_dict)
            except Exception as e :
                pass
        print(len(data_list))
        ret={}
        
        ret['num']=len(self.results)#math.ceil((len(self.results))/20)
        ret['data']=data_list
        # ret['author_to_essay']=imsb1.author_to_essay
        # ret['key_to_essay']=imsb1.key_to_essay
        # ret['year_to_essay']=imsb1.year_to_essay
        # ret['org_to_essay']=imsb1.org_to_essay
        return JsonResponse(ret,safe=False)

class MySuggestSeachView(SearchView):
    
    def create_response(self):
        context = self.get_context()
        data_list=[]
        for i in context['page'].object_list:
            try:
                data_dict={}
                data_dict['value']=i.title[0:80]
                
                data_list.append(data_dict)
            except Exception as e :
                pass
        print(data_list)
        return JsonResponse(data_list,safe=False)

class MorelikethisSeachView(SearchView):
    
    def create_response(self):
        print("im in morelikethis")
        context = self.get_context()
        data_list=[]
        for i in context['page'].object_list:
            try:
                strkey=i.object.keywords
                strauth=i.object.auth
                # print(strkey)
                # print(strauth)
                if(strkey==-1):
                    strkey="[]"
                if(strauth==-1):
                    strauth="[]"
                
                arrkey =  eval('(' + strkey + ')')
                arrauth =  eval('(' + strauth + ')')
                # print(arrkey)
                # print(arrauth)
                data_dict={}            
                data_dict['title']=i.object.title
                data_dict['id']=i.object.id
                data_dict['auth']=arrauth
                data_dict['year']=i.object.year
                data_dict['keywords']=arrkey
                data_dict['fos']=i.object.fos
                data_dict['n_citation']=i.object.n_citation
                data_dict['publisher']=i.object.publisher
                data_dict['issue']=i.object.issue
                data_dict['abstract']=i.object.abstract
                data_dict['doi']=i.object.doi
                data_list.append(data_dict)
                print(data_dict)
            except Exception as e :
                print(e)
        print(data_list)
        return JsonResponse(data_list,safe=False)