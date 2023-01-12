# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth import forms as auth_forms
from users.models import CustomUser

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg form-control-solid",
                "autocomplete": "off"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control form-control-lg form-control-solid"
            }
        ))


class SignUpModelForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg form-control-solid",
                }
        ),
        required=True,
    )
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg form-control-solid",
                "id": "nickname"
            }
        ),
        required=True,
    )
    cpf = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg form-control-solid",
                "placeholder": "Digite seu cpf...",
                "id": "cpf"
            }
        ),
        required=True,
        max_length=14,
        min_length=11
    )
    birth_date = forms.CharField(
        widget=forms.DateInput(
            attrs={
                "id": "data_nascimento_afiliado",
                "type": "date",
                "class": "form-control form-control-lg form-control-solid",
                "Placeholder": "Ex.: 00/00/0000",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg form-control-solid",
                "placeholder": "nome@email.com",
                "autocomplete": "off",
                "id": "email"
            }
        ),
        required=True,
        
    )
    fone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg form-control-solid js-cellphones",
                "value": "55",
                "placeholder": "Ex.: +55 (00) 00000-0000",
                "id": "celular",
            }
        ),
        required=True,
        max_length=19,
        min_length=13
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control form-control-lg form-control-solid",
            }
        ),
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control form-control-lg form-control-solid",
            },
        ),
        required=True,
    )

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        # Remover os pontos e o hífen do CPF
        cpf = cpf.replace('.', '').replace('-', '')
        return cpf

    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


    class Meta:
        model = CustomUser
        fields = ('name', 'nickname', 'fone', 'birth_date', 'cpf', 'email', 'password1', 'password2')


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-solid",
                "autocomplete": "off"
            }
        ))


class PasswordResetConfirmForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control w-100"}),)
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control w-100"}),)
