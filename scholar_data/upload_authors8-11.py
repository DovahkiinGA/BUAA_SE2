import os
from django.test import TestCase
import os,django,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()
from scholar_data.models import *

def readAuthors(addr):
    file = open(addr)
    file_str = file.read()
    file_str = file_str.split('\n')
    print('start import')
    for i in range(len(file_str)):
        try:
            name = normalized_name = orgs = position = tags = pubs = "-1"
            n_pubs = n_citation = -1
            is_claimed = 0
            dict = eval(file_str[i])
            if 'name' in dict:
                name = dict['name']
            if 'normalized_name' in dict:
                normalized_name = dict['normalized_name']
            if 'orgs' in dict:
                orgs = dict['orgs']
            if 'position' in dict:
                position = dict['position']
            if 'n_pubs' in dict:
                n_pubs = dict['n_pubs']
            if 'n_citation' in dict:
                n_citation = int(dict['n_citation'])
            if 'tags' in dict:
                tags = str(dict['tags'])
            if 'pubs' in dict:
                pubs = str(dict['pubs'])
            Authors.objects.create(id=dict['id'], name=name,
            normalized_name=normalized_name,orgs=orgs,position=position,n_pubs=n_pubs,tags = tags,pubs=pubs)
        except:
            print("bad data")
        
        if i % 1000 == 0:
            print(str(i) + " data imported")
    file.close()


def readFiles():
    print(os.listdir("/meow/sourceData/authors/"))
    files = ["/meow/sourceData/authors/aminer_authors_8.txt", "/meow/sourceData/authors/aminer_authors_9.txt",
             "/meow/sourceData/authors/aminer_authors_10.txt", "/meow/sourceData/authors/aminer_authors_11.txt"]
    for file_name in files:
        print(file_name + ":")
        readAuthors(file_name)

readFiles()
