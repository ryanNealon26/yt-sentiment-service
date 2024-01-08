from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name ='home'), 
    path("select/", views.selectPage, name ='selectPage'), 
    path("read/", views.readComments, name ='readComments'), 
    path("positive-comments/", views.positiveComments, name ='positiveComments'), 
    path("negative-comments/", views.negativeComments, name ='negativeComments'), 
    path("video-data/", views.videoData, name ='videoData'), 
    path("google-charts/", views.googleCharts, name ='googleCharts'), 


]