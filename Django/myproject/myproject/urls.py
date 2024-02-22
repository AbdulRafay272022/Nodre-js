"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path#isse config krty path ko

urlpatterns = [#is list mai url add krdo jo bhi dene
    path('',views.index ,name='index'),#home tw main link hi tw empty or usky sth jo resopnse render krna woh jo bhi views ky index function dega woh is url ko assign hoga name iss id inshort
    path('counter',views.counter,name="counter")#yh url counter ky liyh banaya jaha frint sy data ayega count ka
]
