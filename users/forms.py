from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 
            'is_medico', 'is_assistente_social', 'is_nutricionista',
        )

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'foto', 'is_medico',
            'is_assistente_social', 'is_nutricionista',
        )
