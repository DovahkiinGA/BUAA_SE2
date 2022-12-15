import os
from django.test import TestCase
import os,django,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()
from scholar_data.models import *

def readPapers(addr):
    file = open(addr)
    file_str = file.read()
    file_str = file_str.split('\n')
    print('start import')
    for i in range(len(file_str)):
        try:
            title = auth = keywords = fos = references = page_stat = page_end = doc_type = "-1"
            lang = publisher = volume = issue = issn = isbn = doi = pdf = url = abstract = "-1"
            year = n_citation = -1
            diction = eval(file_str[i])
            if 'title' in diction:
                title = diction['title']
            if 'authors' in diction:
                auth = str(diction['authors'])
            if 'keywords' in diction:
                keywords = str(diction['keywords'])
            if 'fos' in diction:
                fos = str(diction['fos'])
            if 'references' in diction:
                references = str(diction['references'])
            if 'page_start' in diction:
                page_stat = diction['page_start']
            if 'page_end' in diction:
                page_end = str(diction['page_end'])
            if 'doc_type' in diction:
                doc_type = str(diction['doc_type'])
            if 'lang' in diction:
                lang = str(diction['lang'])
            if 'publisher' in diction:
                publisher = diction['publisher']
            if 'volume' in diction:
                volume = str(diction['volume'])
            if 'issue' in diction:
                issue = str(diction['issue'])
            if 'issn' in diction:
                issn = str(diction['issn'])
            if 'isbn' in diction:
                isbn = str(diction['isbn'])
            if 'doi' in diction:
                doi = diction['doi']
            if 'pdf' in diction:
                pdf = str(diction['pdf'])
            if 'url' in diction:
                url = str(diction['url'])
            if 'abstract' in diction:
                abstract = str(diction['abstract'])
            if 'year' in diction:
                year = str(diction['year'])
            if 'n_citation' in diction:
                n_citation = str(diction['n_citation'])
            try:
                Papers.objects.create(id=diction['id'], title=title,
                auth=auth,keywords=keywords,fos=fos,references=references,
                page_stat = page_stat,page_end=page_end,doc_type=doc_type,lang=lang,
                publisher=publisher,volume=volume,issn = issn,issue=issue,isbn=isbn,doi=doi,pdf=pdf,
                url=url,abstract=abstract,year=year,n_citation=n_citation)
            except:
                p = Papers.objects.filter(id = diction['id'])
                p.update(auth = auth,page_stat = page_stat,issn = issn)
        except:
            print("bad data")

        if i % 1000 == 0:
            print(str(i) + " data imported")

    file.close()


def readFiles():
    print(os.listdir("/meow/sourceData/papers/"))
    files = ["/meow/sourceData/papers/aminer_papers_0.txt", "/meow/sourceData/papers/aminer_papers_1.txt",
             "/meow/sourceData/papers/aminer_papers_2.txt","/meow/sourceData/papers/aminer_papers_3.txt"]
    for file_name in files:
        print(file_name + ":")
        readPapers(file_name)
    print("-------------------done------------------")

readFiles()
