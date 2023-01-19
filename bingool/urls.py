from django.urls import path
from .views import GameTemplateView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('game/', GameTemplateView.as_view(), name="game"),
]
