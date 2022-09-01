from asyncio.windows_events import NULL
from django.db import models
from coreapp.models import Txt
from django.core.files import File
def run():
    with open('static/example.txt', 'rb') as f:
        txt = Txt(title='Example', text='these are 50 curves form exoTrain (data set of light curves) file with only the 50 inicial values.',  file=File(f , name= 'example.txt'))
        txt.save()
        f.close()