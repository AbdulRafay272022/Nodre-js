from django.shortcuts import render
from . models import Book
from django.db import connection
# Create your views here.

def book_list(request):
    with connection.cursor() as cur:
        cur.execute('SELECT * FROM Books')
        books=cur.fetchall()
    return render(request,'book_list.html',{'books':books})    