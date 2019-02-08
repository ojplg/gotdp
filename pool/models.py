from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    pass

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
