from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Txt
import pickle
import numpy as np
from scripts.cluster import clusterthis
import os
from coreapp.forms import CreateForm



class MainView(View):
    def get(self, request):
        ctx = {
            
        }        
        return render(request, 'coreapp/home.html', ctx)

class Explanation(View):
    def get(self, request):
        ctx = {

        }        
        return render(request, 'coreapp/explanation.html', ctx)

class About(View):
    def get(self, request):
        ctx = {

        }        
        return render(request, 'coreapp/about.html', ctx)

class Application(ListView):
    model = Txt
    template_name = 'coreapp/application.html'

class Uploadfile(LoginRequiredMixin, View):
    template_name = 'coreapp/form.html'
    success_url = reverse_lazy('coreapp:application')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        file = form.save(commit=False)
        file.owner = self.request.user
        file.save()
        return redirect(self.success_url)

class DeletefileView(DeleteView):
    model = Txt
    template_name = "coreapp/delete.html"
    def get_queryset(self):
        qs = super(DeletefileView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class Addapp(View):
    def get(self, request):
        try:
            title = request.GET.get('title','')
            obj = Txt.objects.get(title=title)
            if os.path.exists('static/'+title) == False:
                file = obj.file
                title = obj.title
                title= title.lower()
                try:    
                    fileloaded = pickle.load(file)
                except:
                    text = 'Failed to pickle.load file, make sure you uploaded a pickle.dump .txt file '
                    return JsonResponse({'add1': text})
                try:
                    print('3')
                    clusterthis(fileloaded , title)
                    text = 'Cluster of '+title+' done successfully'
                    print('4')
                except:
                    text = 'Cluster of '+title+' Faill'
                    return JsonResponse({'add1': text})
            title = obj.title
            title= title.lower()
            with open('static//'+title+'//'+title+"-info.txt", 'rb') as fp:
                info= pickle.load(fp)
                fp.close()
            a= np.argmax(info[1])
            radius = info[0][a]
            with open('static//'+title+'//'+title+'-'+str(radius)+"groups.txt", 'rb') as fp:
                group= pickle.load(fp)
                fp.close()
            title= str(title)
            group = str(group)
            radius = str(radius)
            
            ctx={
                'title': title,
                'group': group,
                'radius': radius,
            }
            text1 = render_to_string("coreapp/add1.html", ctx)
        except:
            text1 = 'Fail'
        return JsonResponse({'add1': text1})
    

class ClusterRun(View):
    def get(self, request):
        title = request.GET.get('title','')
        if os.path.exists('static/'+title) == False:
            print(title)
            obj = Txt.objects.get(title=title)
            file = obj.file
            title = obj.title
            title= title.lower()
            fileloaded = pickle.load(file)
            try:
                clusterthis(fileloaded , title)
                text = 'Cluster of '+title+' done successfully'
            except:
                text = 'Cluster of '+title+' Faill'
                return JsonResponse({'add1': text})
        else: return JsonResponse({'add1': 'Already done.'})

class ResultTest(ListView):
    model = Txt
    template_name = "coreapp/resulttest.html"

class DownloadResults(View):
    def get(self, request, title):
        title = title
        print('1')
        if os.path.exists('static/'+title) == True:
            print('2')
            zip_file = open('static//'+title+'//results.tar.gz', 'rb')
            response = HttpResponse(zip_file, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="%s"' % 'results.tar.gz'
            return response

    
