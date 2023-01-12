from django.urls import path
from .views import PainelUsersView

urlpatterns = [
    path('painel-usuario/', PainelUsersView.as_view(), name="painel_user"),
]
    