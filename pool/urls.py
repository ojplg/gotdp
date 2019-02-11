from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('select_characters', views.select_characters, name='select_characters'),
    path('profile',views.profile,name='profile'),
    path('logout',views.do_logout,name='do_logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register_user', views.register_user, name='register_user'),
    path('summary',views.summary, name='summary'),
    path('scoreboard',views.scoreboard, name='scoreboard'),
    path('rules_disclaimers',views.rules_disclaimers, name='rules_disclaimers'),
]
