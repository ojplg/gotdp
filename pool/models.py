from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return 'Character: ' + self.name

