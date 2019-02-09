from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('select_characters', views.select_characters, name='select_characters'),
    path('profile',views.profile,name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register_user', views.register_user, name='register_user'),
]
