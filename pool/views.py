from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from collections import Counter

from .models import Character, CustomUser, Selection, Selections
from .forms import CharacterSelectsForm, RegisterUserForm, CouplesForm
from .scoring import calculate_score, character_sums, calculate_couple_counts

import logging

logger = logging.getLogger('pool')

def index(request):
    return render(request,'index.html',{})

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            logging.info("registering!")
            user = CustomUser.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterUserForm()
        context = { 'form':form }
        return render(request,'register_user.html',context)

@login_required
def select_characters(request):
#    if request.method == 'POST':
#        form = CharacterSelectsForm(request.POST)
#        if form.is_valid():
#            selections = Selections.load_by_user(request.user)
#            post_data = form.cleaned_data
#            selections.update_picks(post_data)
#            context = {'user':request.user}
#            return redirect('profile')
#    else:
        selections = Selections.load_by_user(request.user)
        data = selections.picks_dictionary()
        form = CharacterSelectsForm(data) 
        context = { 'form': form }
        return render(request,'select_characters.html',context) 

@login_required
def select_couples(request):
#    if request.method == 'POST':
#        form = CouplesForm(request.POST)
#        if form.is_valid():
#            logging.debug(str(form.cleaned_data))
#            selections = Selections.load_by_user(request.user)
#            logging.debug(str(selections))
#            selections.update_couples(form.cleaned_data)
#            return redirect('profile')
#    else:
        selections = Selections.load_by_user(request.user)
        data = selections.couples_dictionary()
        form = CouplesForm(data)
        context = { 'form':form }
        return render(request,'select_couples.html',context)

@login_required
def profile(request):
    selections = Selections.load_by_user(request.user)
    characters = Character.objects.all()
    score = calculate_score(selections, characters)
    context = {'user':request.user, 
               'lives':selections.picks_to_live(), 
               'dies':selections.picks_to_die(),
               'couples':selections.couples(),
               'unselected': selections.unselected(),
               'mortality_score':score[0],
               'romance_score':score[1],
               'total_score':score[2]}
    return render(request,'profile.html',context)

def do_logout(request):
    logout(request)
    return render(request,'index.html',{})

def summary(request):
    characters = Character.objects.all()
    summary_counts = character_sums(characters)
    couple_counts = calculate_couple_counts()
    context = {
        'characters':sorted(characters),
        'liveCount': summary_counts[0],
        'deadCount': summary_counts[1],
        'livePercentage': summary_counts[2],
        'coupleCounts':couple_counts
    }
    return render(request,'summary.html',context)

def scoreboard(request):
    allSelections = Selections.objects.all()
    characters = Character.objects.all()
    scores = {}
    for selections in allSelections:
        scores[selections.user.username] = calculate_score(selections,characters)
    context = { 'scores':scores }
    return render(request,'scoreboard.html',context)

def rules_disclaimers(request):
    return render(request,'rules_disclaimers.html',{})
