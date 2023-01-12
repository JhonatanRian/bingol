from django.urls import path
from .views import GameTemplateView

urlpatterns = [
    path('game/', GameTemplateView.as_view(), name="game"),
]
