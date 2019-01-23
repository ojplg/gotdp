from django import forms

from .models import Character

class CharacterSelectsForm(forms.Form):
    characters = forms.ModelMultipleChoiceField(Character.objects.order_by('name'))
