from django.urls import path
from .views_api import match_current, next_match, sync, bingo, cards, auth_me

urlpatterns = [
    path('auth/Me/', auth_me, name='auth_me'),
    path('match_current/', match_current, name='match'),
    path('match_sync', sync, name='sync'),
    path('bingo/', bingo, name='bingo'),
    path('cards/', cards, name='cards'),
    path('nextMatch/', next_match, name='next_match')
]