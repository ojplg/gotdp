from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    pass

class Character(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return 'Character: ' + self.name

    def __lt__(self, other):
        return self.name.__lt__(other.name)

class Selections(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "Selections: " + str(user) + " are " + str(picks)    
    
    def picks(self):
        return Selection.objects.filter(selections=self)

    def picks_to_live(self):
        lives = []
        for pick in self.picks():
            if ( pick.outcome == 'L' ):
                lives.append(pick.character)
        return sorted(lives)
            
    def picks_to_die(self):
        dies = []
        for pick in self.picks():
            if ( pick.outcome == 'D' ):
                dies.append(pick.character)
        return sorted(dies)

    def pick_by_name(self, name):
        for pick in self.picks():
            if ( pick.character.name == name ):
                return pick.outcome
        return None

    def picks_dictionary(self):
        data = {}
        for pick in self.picks():
            data[pick.character.name]=Selection.decode_outcome(pick.outcome)
        return data

    def unselected(self):
        missing = []
        characters = Character.objects.all()
        selections = self.picks()
        selected_characters = map ( lambda sel: sel.character , selections )
        for character in characters:
            if (character not in selected_characters):
                missing.append(character)
        return missing
            
    def update_picks(self, data):
        for name, prediction in data.items():
            new_name = True
            for pick in self.picks():
                if ( pick.character.name == name ):
                    pick.outcome = prediction[0]
                    new_name = False
                    print("Resetting value for " + name + " to " + prediction)
                    pick.save()
            if ( new_name ):
                selection = Selection()
                character = Character.objects.get(name=name)
                selection.character = character
                selection.outcome = prediction[0]
                selection.selections = self
                selection.save()
 
    def load_by_user(user):
        try:
            return Selections.objects.get(user=user)
        except DoesNotExist:
            selections = Selections()
            selections.user = user
            return selections

class Selection(models.Model):
    OUTCOMES = (
        ('L','Lives'),
        ('D','Dies'))
    character = models.ForeignKey(Character,on_delete=models.CASCADE)
    selections = models.ForeignKey(Selections,on_delete=models.CASCADE)
    outcome = models.CharField(choices=OUTCOMES,max_length=1)

    def __str__(self):
        return "Selection " + self.character.name + " should " + self.outcome

    def __lt__(self, other):
        return self.character.__lt__(other.character)

    def decode_outcome(code):
        if ( code == 'L' ):
            return 'Lives'
        if ( code == 'D' ):
            return 'Dies'
        raise Exception("Unrecognized code " + code)

       
