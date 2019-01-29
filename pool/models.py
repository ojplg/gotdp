from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return 'Character: ' + self.name

class Selection(models.Model):
    OUTCOMES = (
        ('L','Lives'),
        ('D','Dies'))
    character = models.OneToOneField(Character,on_delete=models.CASCADE)
    outcome = models.CharField(choices=OUTCOMES,max_length=1)

class Selections(models.Model):
    picks = models.ManyToManyField(Selection, verbose_name="list of selections")
