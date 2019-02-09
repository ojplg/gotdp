from django import forms

from .models import Character

class CharacterSelectsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CharacterSelectsForm, self).__init__(*args, **kwargs)
        CHOICES = (('Lives','Lives'),('Dies','Dies'))
        for c in Character.objects.order_by('name'):
            self.fields[c.name] = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False)

    def populate_selections(self,selections):
        for name in self.fields:
            prediction = selections.pick_by_name(name)
            print(" FORM PREDICTION FOR " + name + " was " + prediction)
            
        

class RegisterUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
