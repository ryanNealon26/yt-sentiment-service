from django.shortcuts import render, redirect
from django.http import HttpResponse
from .Video import Video
import validators
user = Video()
def home(request):
    data = request.POST.get('url-input')
    if validators.url(data):
        user.video_url = data
        return redirect(selectPage)
    return render(request,"home.html") 
def selectPage(request):
    return render(request, "select-screen.html")
def readComments(request):
    commentData  = user.create_comments_list()
    return render(request,'read-comments.html', commentData)
def positiveComments(request):
    posCommentData = user.view_positive_comments()
    return render(request, 'positive.html', posCommentData)
def negativeComments(request):
    negCommentData = user.view_negative_comments()
    return render(request, 'negative.html', negCommentData)
def videoData(request):
    videoData = user.video_statistics()
    return render(request, 'video-data.html', videoData)