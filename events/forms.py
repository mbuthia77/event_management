from django import forms
from .models import User, CustomUser
from django.contrib.auth.forms import UserCreationForm

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
