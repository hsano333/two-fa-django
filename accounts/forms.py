from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms

# from .modelss import User, FtUser
from .models import FtUser, FtTmpUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = FtUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class SignUpTmpForm(UserCreationForm):
    class Meta:
        model = FtTmpUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class LoginForm(AuthenticationForm):

    class Meta:
        model = FtUser
