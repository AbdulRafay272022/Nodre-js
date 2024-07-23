from django.shortcuts import render
from .models import Post
# Create your views here.
def home(request):
    posts=Post.objects.all()#retrun all in post table
    return render(request,'home.html',{'posts':posts})

def post(request,pk):
    posts=Post.objects.get(id=pk)
    return render(request,'post.html',{'posts':posts})