from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from collections import Counter

from .models import Character, CustomUser, Selection, Selections
from .forms import CharacterSelectsForm, RegisterUserForm, CouplesForm

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
                selections.user = request.user
                selections.save()
            post_data = form.cleaned_data
            selections.update_picks(post_data)
            context = {'user':request.user}
            return redirect('profile')
    else:
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
def select_couples(request):
    if request.method == 'POST':
        form = CouplesForm(request.POST)
        if form.is_valid():
            print(str(form.cleaned_data))
            selections = Selections.load_by_user(request.user)
            print(str(selections))
            selections.update_couples(form.cleaned_data)
            return redirect('profile')
    else:
        form = CouplesForm()
        print('form:: ' + str(form))
        context = { 'form':form }
        return render(request,'select_couples.html',context)

@login_required
def profile(request):
    selections = Selections.load_by_user(request.user)
    context = {'user':request.user, 
               'lives':selections.picks_to_live(), 
               'dies':selections.picks_to_die(),
               'unselected': selections.unselected()}
    return render(request,'profile.html',context)

def do_logout(request):
    logout(request)
    return render(request,'index.html',{})

def summary(request):
    characters = Character.objects.all()
    allSelections = Selection.objects.all()
    deadCount = Counter()
    liveCount = Counter()
    for character in characters:
        deadCount[character] = 0
        liveCount[character] = 0
    for selection in allSelections:
        if selection.outcome == 'L' :
            liveCount[selection.character] += 1
        if selection.outcome == 'D' :
            deadCount[selection.character] += 1
    livePercentage = {}
    for character in characters:
        liveVotes = liveCount[character]
        deadVotes = deadCount[character]
        total = liveVotes + deadVotes
        if total == 0:
            livePercentage[character] = 0
        else: 
            livePercentage[character] = 100 * liveVotes / ( liveVotes + deadVotes )
    context = {
        'characters':sorted(characters),
        'liveCount': liveCount,
        'deadCount': deadCount,
        'livePercentage':livePercentage
    }
    return render(request,'summary.html',context)

def scoreboard(request):
    allSelections = Selections.objects.all()
    characters = Character.objects.all()
    scores = {}
    for selections in allSelections:
        scores[selections.user.email] = selections.compute_score(characters)
    context = { 'scores':scores }
    return render(request,'scoreboard.html',context)

def rules_disclaimers(request):
    return render(request,'rules_disclaimers.html',{})
