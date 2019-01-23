from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("GOT Death Pool Index")

def select_characters(request):
    context = {}
    return render(request,'select_characters.html',context) 
