from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .models import Character
from .forms import CharacterSelectsForm, RegisterUserForm

def index(request):
    return HttpResponse("GOT Death Pool Index")

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print("registering!")
            print( form.cleaned_data )
            user = User.objects.create_user(form.cleaned_data['email'],form.cleaned_data['email'],form.cleaned_data['password'])
            print("user!")
            print(user)
            user.save()
        return HttpResponseRedirect('select_characters')
    else :
        form = RegisterUserForm()
        context = { 'form':form }
        return render(request,'register_user.html',context)

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


