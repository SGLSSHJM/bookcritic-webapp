from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Remark
from django.template import loader
# Create your views here



def index(request):
    return render(request, 'books/index.html', {
        "books": Book.objects.all(),
    })
def remark(request, remark_id):
    response = "You are looking at the %s remark."  
    return HttpResponse(response % remark_id)
def bookdetail(request, book_id):
    book=Book.objects.get(pk=book_id)
    return render(request, 'books/bookdetail.html', {
        "book":book,
    })
