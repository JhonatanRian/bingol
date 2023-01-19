# -*- encoding: utf-8 -*-

from django.contrib.auth import authenticate, login
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .forms import LoginForm, SignUpModelForm, PasswordResetForm, PasswordResetConfirmForm
from rest_framework.authtoken.models import Token

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                Token.objects.get(user=user).delete()
                Token.objects.create(user=user)
                return redirect("/users/painel-usuario")
            else:
                msg = 'Usuario ou senha inválidos'
        else:
            msg = 'Erro ao logar'

    return render(request, "accounts/sign-in.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            form.save()

            msg = 'Usuario cadastrado com sucesso'
            messages.success(request, msg)
            return redirect("/accounts/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpModelForm()

    return render(request, "accounts/sign-up.html", {"form": form, "msg": msg, "success": success})


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = "password/password-reset.html"
    email_template_name = "password_reset_email.txt"



class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name="password/password-reset-confirm.html"