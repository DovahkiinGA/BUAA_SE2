from django.test import TestCase
import os,django,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()
from scholar_data.models import *

def readVenues():
    print("---------------------Venues,begin---------------------")
    venues = open('/meow/sourceData/venues/aminer_venues.txt')
    file_str = venues.read()
    file_str = file_str.split('\n')
    i = 69500
    print(len(file_str))
    while i<len(file_str):
        try:
            dn = nn = "-1"
            dict = eval(file_str[i])
            if 'DisplayName' in dict:
                dn = dict['DisplayName']
            if 'NormalizedName' in dict:
                nn = dict['NormalizedName']
            Venues.objects.create(id = dict['id'],DisplayName = dn,NormalizedName=nn)
        except:
            print("bad data")
        #else:
            
        if i%1000 ==0:
            print(str(i) +" data imported")
        i = i+1
    venues.close()

readVenues()
print('hh')