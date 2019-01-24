from django.shortcuts import render

from django.http import HttpResponse

from .models import Character

from .forms import CharacterSelectsForm

def index(request):
    return HttpResponse("GOT Death Pool Index")

def select_characters(request):
    if request.method == 'POST':
        form = CharacterSelectsForm(request) 
    else :
        form = CharacterSelectsForm() 

    context = { 'form': form }
    return render(request,'select_characters.html',context) 
