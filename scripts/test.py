from django.db import models
from coreapp.models import Txt
from cluster import clusterthis
import pickle
def run():
    obj = Txt.objects.get(id=1)
    file = obj.file
    Van = pickle.load(file)
    print(len(Van))
    clusterthis(Van , 'example')

