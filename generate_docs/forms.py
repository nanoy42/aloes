"""Forms of the generate_docs app"""
from django import forms

class MailingLabelForm(forms.Form):
    """Form to upload a csv file"""
    file = forms.FileField()
