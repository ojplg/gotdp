from django.shortcuts import render
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
            post_data = form.cleaned_data
            print( "oh boy")
            print( post_data )
            print( "oh boy 2" )
            picks = []
            for k, v in post_data.items():
                character = Character.objects.get(name=k)
                print(" PREDICTION FOR " + str(character) + " is " + v)
                selection = Selection()
                selection.character = character
                selection.outcome = v[0]
                selection.save()
                print( " SELECTION " + str(selection))
                picks.append(selection)
            selections = Selections()
            selections.user = request.user
            selections.save()
            selections.picks.set(picks)
            selections.save()
            context = {'user':request.user}
            return render(request,'profile.html',context)
    else :
        form = CharacterSelectsForm() 
        context = { 'form': form }
        return render(request,'select_characters.html',context) 

def selections_made(request):
    context = {}
    return render(request,'selections_made.html',context)

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
