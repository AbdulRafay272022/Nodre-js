from django.shortcuts import render
from django.http import HttpResponse
from .models import Feature
#create your views here
def index(request):
    # HttpResponse('<h1> Hey,Welcom </h1>')
    context={
        "name":'Usman',
        "age":25,
        "country":'Pakistan'
    }#dynamic data

    F1=Feature()
    F1.name="FAST"
    F1.description="OUR SERVICE IS FAST"
    F1.id=0
    F1.true=True

    F2=Feature()
    F2.name="RELIABLE"
    F2.description="OUR SERVICE IS RELIABLE"
    F2.id=1
    F2.true=True

    F3=Feature()
    F3.name="EASY TO USE"
    F3.description="OUR SERVICE IS EASY TO USE"
    F3.id=2
    F3.true=False

    return render(request,'index.html',{'context':context,'F1':F1,'F2':F2,'F3':F3})#request ka function or yh return kare ka index.html  or isko phale hi bta chuky hum settiung.py mai,data to send wrap it in dictionary so it can be send to front end

def counter(request):
    #text=request.GET['text']#same jo waha name mai diya hai
    text=request.POST['text']
    count=len(text.split())
    return render(request,'counter.html',{'count':count})