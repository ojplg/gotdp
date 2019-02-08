from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .models import Character

admin.site.register(Character)

admin.site.register(CustomUser, UserAdmin)
