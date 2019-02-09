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

class Selection(models.Model):
    OUTCOMES = (
        ('L','Lives'),
        ('D','Dies'))
    character = models.ForeignKey(Character,on_delete=models.CASCADE)
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

class Selections(models.Model):
    picks = models.ManyToManyField(Selection, verbose_name="list of selections")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def picks_to_live(self):
        lives = []
        for pick in self.picks.all():
            if ( pick.outcome == 'L' ):
                lives.append(pick.character)
        return sorted(lives)
            
    def picks_to_die(self):
        dies = []
        for pick in self.picks.all():
            if ( pick.outcome == 'D' ):
                dies.append(pick.character)
        return sorted(dies)

    def pick_by_name(self, name):
        for pick in self.picks.all():
            if ( pick.character.name == name ):
                return pick.outcome
        return None

    def picks_dictionary(self):
        data = {}
        for pick in self.picks.all():
            data[pick.character.name]=Selection.decode_outcome(pick.outcome)
        return data
