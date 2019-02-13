from django import forms

from .models import Character

class CharacterSelectsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CharacterSelectsForm, self).__init__(*args, **kwargs)
        CHOICES = (('Lives','Lives'),('Dies','Dies'))
        for c in Character.objects.order_by('name'):
            self.fields[c.name] = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False, label=c.name)

class RegisterUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CouplesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        CHOICES = [('','')] + list(map ( lambda n: (n,n), Character.allNames() ))
        super(CouplesForm, self).__init__(*args, **kwargs)
        for index in range(10):
            leftIndex = 'left' + str(index)
            rightIndex = 'right' + str(index)
            self.fields[leftIndex] = forms.ChoiceField(choices=CHOICES, required=False)
            self.fields[rightIndex] = forms.ChoiceField(choices=CHOICES, required=False)
    
