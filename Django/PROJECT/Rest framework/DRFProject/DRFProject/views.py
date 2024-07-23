from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    def get(self,request,*args,**kwargs):
        data={
            'username':'admin',
            'number_of_years':10
        }

        return Response(data)