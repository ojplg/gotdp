from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Character
from .models import CustomUser
from .models import Selection
from .models import Selections
from .forms import CharacterSelectsForm, RegisterUserForm

def index(request):
    return render(request,'index.html',{})

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print("registering!")
            print( form.cleaned_data )
            user = CustomUser.objects.create_user(form.cleaned_data['email'],form.cleaned_data['email'],form.cleaned_data['password'])
            print("user!")
            print(user)
            user.save()
        return HttpResponseRedirect('select_characters')
    else :
        form = RegisterUserForm()
        context = { 'form':form }
        return render(request,'register_user.html',context)

@login_required
def select_characters(request):
    if request.method == 'POST':
        form = CharacterSelectsForm(request.POST)
        if form.is_valid():
            selections = Selections()
            try:
                selections = Selections.objects.get(user=request.user)
            except Selections.DoesNotExist:
                print("No selections yet")
            post_data = form.cleaned_data
            selections.user = request.user
            selections.save()
            selections.update_picks(post_data)
            context = {'user':request.user}
            return redirect('profile')
    else :
        data = {}
        try:
            selections = Selections.objects.get(user=request.user)
            data = selections.picks_dictionary()
        except Selections.DoesNotExist:
            print("User " + str(request.user) + " has no picks")
        form = CharacterSelectsForm(data) 
        context = { 'form': form }
        return render(request,'select_characters.html',context) 

@login_required
def profile(request):
    lives = []
    dies = []
    try:
        selections = Selections.objects.get(user=request.user)
        lives = selections.picks_to_live()
        dies = selections.picks_to_die()
    except Selections.DoesNotExist:
        print("User " + str(request.user) + " has no picks")
    context = {'user':request.user, 'lives':lives, 'dies':dies}
    return render(request,'profile.html',context)
