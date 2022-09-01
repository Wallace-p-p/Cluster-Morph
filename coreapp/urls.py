from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.urls import reverse_lazy


app_name = 'coreapp'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('explanation', views.Explanation.as_view(), name='explanation'),
    path('application', views.Application.as_view(), name='application'),
    path('about', views.About.as_view(), name='about'),
    path('add1', views.Addapp.as_view(), name='add1'),
    path('create', views.Uploadfile.as_view(), name='create'),
    path('file/<int:pk>/delete', views.DeletefileView.as_view(success_url=reverse_lazy('coreapp:application')), name='delete'),
    path('test', views.ResultTest.as_view(), name='results'),
    path('run', views.ClusterRun.as_view(), name='run'),
    path('dl/<str:title>', views.DownloadResults.as_view(), name='dl'),
]