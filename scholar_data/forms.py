from django import forms
from haystack.forms import SearchForm
import json
from .models import Papers
from haystack.query import SQ,SearchQuerySet
# from .sbdata import imsb1
class ScholarkeywordSearch(SearchForm):
    title1=""
    author_to_essay1=[]
    sorttype = forms.CharField(required=False)
    need = forms.CharField(required=False)
    # formula = forms.CharField(required=False)

    def search(self):
        print("===searching self imsb")
        if not self.is_valid():
            print("invalid")
            return self.no_query_found()
        formula=json.loads(self.cleaned_data['q'])
        type1=self.cleaned_data['sorttype']
        need=self.cleaned_data['need']
        print(type1)

        dates=formula['dates']
        group=formula['group']
        print("开始时间:"+dates[0])
        print("结束时间:"+dates[1])
        print("有"+str(len(group))+"组或")
        # sqs=SearchQuerySet().filter(title='internet development').load_all()
        # return sqs
        sb=""
        for i in group:
            imsb="("
            for j in i:
                imssb=""
                if(j['kind']=='topic'):
                    j['kind']='title'
                imssb="SQ(" +j['kind']+"='"+j['content']+"')"
                imsb=imsb+imssb +"&"
            imsb=imsb[:-1]
            imsb=imsb+")|"
            sb=sb+imsb
        sb=sb[:-1]
        # print(sb)
        command="sqs=SearchQuerySet().filter("+sb+")"
        if(dates[0]):
            command+=".filter(year__gte="
            command+="("+dates[0][0:4]+"))"
        if(dates[1]):
            command+=".filter(year__lte="
            command+="("+dates[1][0:4]+"))"
        if(type1=="3"):
            command+=".order_by('-n_citation')"
        elif(type1=="4"):
            command+=".order_by('n_citation')"
        elif(type1=="7"):
            command+=".order_by('-year')"
        elif(type1=="8"):
            command+=".order_by('year')"
        # else:
        #     command="sqs=SearchQuerySet().filter("+sb+")"
        print(command)
        d = {}
        exec(command,globals(), d)
        sqs=d['sqs']        

        sqs=sqs.load_all().highlight()
        print("查询到"+str(sqs.count())+"个结果")
        # if (need=="1"):
        #     print("need")
        #     author_to_essay={}
        #     publisher_to_essay={}
        #     year_to_essay={}
        #     key_to_essay={}
        #     org_to_essay={}
        #     for i in sqs:
        #         try :
        #             arrauth =  eval('(' + i.object.auth + ')')
        #             if arrauth!=-1:
        #                 for j in arrauth:
                            
        #                     if j["name"] not in author_to_essay.keys():
        #                         author_to_essay.update({j["name"]:1})
        #                     else:
        #                         author_to_essay[j["name"]]+=1
        #                     if j["org"] not in org_to_essay.keys():
        #                         org_to_essay.update({j["org"]:1})
        #                     else:
        #                         org_to_essay[j["org"]]+=1
        #             arrkey =  eval('(' + i.object.keywords + ')')
        #             if arrkey!=-1:
        #                 for j in arrkey:
        #                     if j not in key_to_essay.keys():
        #                         key_to_essay.update({j:1})
        #                     else:
        #                         key_to_essay[j]+=1

        #             if i.object.year not in year_to_essay.keys():
        #                 year_to_essay.update({i.object.year:1})
        #             else:
        #                 year_to_essay[ i.object.year]+=1

        #             if i.object.publisher not in publisher_to_essay.keys():
        #                 publisher_to_essay.update({i.object.publisher:1})
        #             else:
        #                 publisher_to_essay[ i.object.publisher]+=1
        #         except Exception as e :
        #             pass
        #     imsb1.author_to_essay=sorted(author_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        #     imsb1.key_to_essay=sorted(key_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        #     imsb1.year_to_essay=sorted(year_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        #     imsb1.org_to_essay=sorted(org_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        # else:
        #     print("noneed")
        #     imsb1.author_to_essay=[]
        #     imsb1.key_to_essay=[]
        #     imsb1.year_to_essay=[]
        #     imsb1.org_to_essay=[]
    
        return sqs

        

class ScholarSuggestSearch(SearchForm):
    def search(self):
        if not self.is_valid():
            print("invalid")
            return self.no_query_found()
        formula=(self.cleaned_data['q'])
        print(formula)
        sqs = SearchQuerySet().filter(content_auto=formula)[0:10]
        suggestions = [result.title for result in sqs]
        # print(suggestions)
        return sqs
        
class MorelikethisSearch(SearchForm):
    def search(self):
        if not self.is_valid():
            print("invalid")
            return self.no_query_found()
        formula=(self.cleaned_data['q'])
        print(formula)
        sqstotal=[]
        paper = Papers.objects.filter(id=formula).first()
        command="sqs=SearchQuerySet().filter("
        paper.auth =  eval('(' + paper.auth+ ')')
        paper.keywords =  eval('(' + paper.keywords+ ')')
        if(paper.auth!=-1):
            name1=paper.auth[0].name
            # sqs = SearchQuerySet().filter(name=name1).load_all()
            # sqstotal=sqstotal+sqs
            command+="(SQ(auth='"+name1+"'))|"
        if(paper.keywords!=-1):
            for i in paper.keywords:
                command+="(SQ(keywords='"+i+"'))|"

        command=command[0:-1]
        command+=")"
        if(paper.auth==-1 and paper.keywords==-1):
            return SearchQuerySet().none()
        else:
            print(command)
            d = {}
            exec(command,globals(), d)
            sqs=d['sqs']        

            sqs=sqs.load_all().highlight()
            print("查询到"+str(sqs.count())+"个结果")

            return sqs[0:20]