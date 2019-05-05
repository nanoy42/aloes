"""Forms of aloes app."""
from django import forms

from .models import GeneralPreferences


class HomeTextEditForm(forms.ModelForm):
    """Display a form to edit home text."""
    class Meta:
        model = GeneralPreferences
        fields = ('home_text', 'english_home_text')

class LoginForm(forms.Form):
    """Display a login form."""
    username = forms.CharField(label="Nom d'utilisateur", max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    """
    Form to change password.

    Ask for current password and to repeat new password
    """
    current_password = forms.CharField(label="Mot de passe actuel", widget=forms.PasswordInput)
    next_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    next_password_repeat = forms.CharField(
        label="Nouveau mot de passe (répétez)",
        widget=forms.PasswordInput
    )
