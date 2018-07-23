from django import forms
from django.contrib.auth.models import User

from .models import GeneralPreferences

class HomeTextEditForm(forms.ModelForm):
    class Meta:
        model = GeneralPreferences
        fields = ('homeText', )

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label="Mot de passe actuel", widget=forms.PasswordInput)
    next_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    next_password_repeat = forms.CharField(label="Nouveau mot de passe (répétez)", widget=forms.PasswordInput)
