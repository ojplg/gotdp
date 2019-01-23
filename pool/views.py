from django.shortcuts import render

from django.http import HttpResponse

from .models import Character

def index(request):
    return HttpResponse("GOT Death Pool Index")

def select_characters(request):
    character_list = Character.objects.order_by('name')
    context = {'character_list':character_list}
    return render(request,'select_characters.html',context) 
