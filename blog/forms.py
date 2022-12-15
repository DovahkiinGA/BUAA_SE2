from django import forms
from haystack.forms import SearchForm
import json
from haystack.query import SQ,SearchQuerySet
class keywordSearch(SearchForm):
    # formula = forms.CharField(required=False)
    def search(self):
        print("===searching self")
        if not self.is_valid():
            print("invalid")
            return self.no_query_found()
        formula=json.loads(self.cleaned_data['q'])

        dates=formula['dates']
        group=formula['group']
        print("开始时间:"+dates[0])
        print("结束时间:"+dates[1])
        print("有"+str(len(group))+"组或")
        sb=""
        for i in group:
            imsb="("
            for j in i:
                imssb=""
                print(j)
                if(j['kind']=='key'):
                    pass
                imssb="SQ(" +j['kind']+"='"+j['content']+"')"
                imsb=imsb+imssb +"&"
            imsb=imsb[:-1]
            imsb=imsb+")|"
            sb=sb+imsb
        sb=sb[:-1]
        print(sb)
        command="sqs=SearchQuerySet().filter("+sb+").load_all()"
        print(command)
        d = {}
        exec(command,globals(), d)
        sqs=d['sqs']
        print("查询到"+str(sqs.count())+"个结果")
        #results = SearchQuerySet().exclude(content='hello').filter(content='world').date_facet('pub_date', start_date=datetime.date(2009, 6, 7), end_date=datetime.date(2009, 7, 7), gap_by='day').order_by('-pub_date').boost('title', 0.5)[10:20]
        return sqs