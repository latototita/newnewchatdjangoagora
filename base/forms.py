from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=["username","email","password1","password2"]


class ProfilePicForm(forms.ModelForm):
	photo=forms.ImageField(required=True)

	class Meta:
		model=Photo
		fields=["photo"]
