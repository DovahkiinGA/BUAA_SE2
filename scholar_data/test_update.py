from django.test import TestCase
import os,django,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()
from scholar_data.models import *

paper = Papers.objects.get(id = "53e99784b7602d9701f3e13e")
print(paper.title)
print(paper.auth)
print(paper.page_stat)
print(paper.issn)