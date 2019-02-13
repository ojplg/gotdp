from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    pass

class Character(models.Model):
    OUTCOMES = (
        ('L','Lives'),
        ('D','Dies'))
    name = models.CharField(max_length=500)
    status = models.CharField(choices=OUTCOMES,max_length=1)

    def __str__(self):
        return 'Character: ' + self.name

    def __lt__(self, other):
        return self.name.__lt__(other.name)

    def allNames():
        cs = Character.objects.all()
        ns = map(lambda c: c.name, cs)
        return list(ns)

    def find_by_name(n):
        print ("Searching for " + n)
        c = Character.objects.get(name=n)
        print ("Found " + str(c))
        return c

class Selections(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "Selections: " + str(self.user) 
    
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
        selected_characters = list ( map ( lambda sel: sel.character , selections ))
        for character in characters:
            if (character not in selected_characters):
                missing.append(character)
        return sorted(missing)
            
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
                if( prediction ):
                    selection = Selection()
                    character = Character.objects.get(name=name)
                    selection.character = character
                    selection.outcome = prediction[0]
                    selection.selections = self
                    selection.save()
         
    def load_by_user(user):
        try:
            return Selections.objects.get(user=user)
        except Selections.DoesNotExist:
            selections = Selections()
            selections.user = user
            selections.save()
            return selections

    def couples(self):
        print ("loading couples for " + str(self))
        return Couple.objects.filter(selections=self)

    def couples_dictionary(self):
        dictionary = {}
        for idx, couple in enumerate(self.couples()):
            dictionary['left' + str(idx)] = couple.left.name
            dictionary['right' + str(idx)] = couple.right.name
        return dictionary            

    def update_couples(self, data):
        submitted_couples = []
        for i in range(10):
            print ("updating couple " + str(i))
            left_character = data.get('left' + str(i))
            right_character = data.get('right' + str(i))
            if ( left_character and right_character ):
                one = Character.find_by_name(left_character)
                two = Character.find_by_name(right_character)
                couple = Couple()
                couple.selections = self
                couple.set_characters(one, two)
                print("adding " + str(couple))
                submitted_couples.append(couple)
        saved_couples = self.couples()
        couples_to_delete = []
        for c in submitted_couples:
            print("checking " + str(c))
            if c not in list(saved_couples):
                print("saving " + str(c))
                c.save()
        for c in saved_couples:
            if c not in (list(submitted_couples)):
                c.delete()
                

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

class Couple(models.Model):
    selections = models.ForeignKey(Selections,on_delete=models.CASCADE)
    left = models.ForeignKey(Character,on_delete=models.CASCADE,related_name='left_character')
    right = models.ForeignKey(Character,on_delete=models.CASCADE,related_name='right_character')

    def set_characters(self, one, two):
        characters = [one, two]
        characters.sort()
        self.left = characters[0]
        self.right = characters[1]

    def __str__(self):
        return "Couple: " + str(self.selections) + ": " + str(self.left) + " & " + str(self.right)
       
