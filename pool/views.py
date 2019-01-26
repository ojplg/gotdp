from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from .models import Character

from .forms import CharacterSelectsForm

def index(request):
    return HttpResponse("GOT Death Pool Index")

def select_characters(request):
    if request.method == 'POST':
        form = CharacterSelectsForm(request.POST)
        if form.is_valid():
            print( "oh boy")
            print( form.cleaned_data )
            print( "oh boy 2" )
        context = { 'form': form }
        return HttpResponseRedirect('select_characters')
         
    else :
        form = CharacterSelectsForm() 
        context = { 'form': form }
        return render(request,'select_characters.html',context) 

def selections_made(request):
    context = {}
    return render(request,'selections_made.html',context)
