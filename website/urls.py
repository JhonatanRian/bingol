from django.urls import path

from website import views as website_views

urlpatterns = [
    path('', website_views.home, name="website"),
    path('', website_views.home, name="website"),
]
