from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # Add this line if you want email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Add 'email' here