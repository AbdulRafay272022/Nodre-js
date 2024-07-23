from django.shortcuts import render
import json #q  ky api sy input json mai atta
import urllib.request

# Create your views here.
def home(request):
    if request.method=='POST':
        city=request.POST['city']
        res=urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=16f40e6883687c3c90816d1e4443510b').read()
        json_data=json.loads(res)
        #print("data fetch",json_data,city,res)
        data={#make dictionary  of json data
            'country_code':str(json_data['sys']['country']),
            'coordinate': str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
            'temp':str(json_data['main']['temp'])+'k',
            'pressure':str(json_data['main']['pressure']),
            'humidity':str(json_data['main']['humidity'])
        }
    else:  
        city=''
        data={}    
        #print("data fetch")
    return render(request,'home.html',{'data':data})