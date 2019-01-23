from django import forms

from .models import Character

#    characters = forms.ModelMultipleChoiceField(Character.objects.order_by('name'))

class CharacterSelectsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CharacterSelectsForm, self).__init__(*args, **kwargs)
        CHOICES = (('Lives','Lives'),('Dies','Dies'))
        for c in Character.objects.order_by('name'):
            self.fields[c.name] = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    
