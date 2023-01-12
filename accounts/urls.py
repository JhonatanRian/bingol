from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views as accounts_views

urlpatterns = [
    path('login/', accounts_views.login_view, name="login"),
    path('register/', accounts_views.register_user, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('password_reset/', accounts_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', accounts_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name="password/password-reset-complete.html"), name="password_reset_complete"),
]
