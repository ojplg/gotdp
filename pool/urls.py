from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('select_characters', views.select_characters, name='select_characters'),
    path('selections_made', views.selections_made, name='selections_made'),
]
