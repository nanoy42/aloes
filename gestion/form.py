from django import forms

from aloes.widgets import DatePicker
from .models import Renovation, School, Tenant, Room, Leasing

class RenovationForm(forms.ModelForm):
    class Meta:
        model = Renovation
        fields = "__all__"

class SearchForm(forms.Form):
    SORTING_CHOICES = (
        ('room', 'Chambre'),
        ('first_name', 'Prénom'),
        ('last_name', 'Nom'),
    )
    BUILDING_CHOICES = (
        ('I', 'Tous'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('G', 'G'),
    )

    PAYMENT_CHOICES = (
        ('I', 'Tous'),
        ('direct_debit', 'Prélèvement'),
        ('bank_transfer', 'Virement'),
        ('check', 'Chèque'),
        ('cash', 'Espèces'),
        ('special', 'Special'),
    )

    GENDER_CHOICES = (
        ('I', 'M/F'),
        ('M', 'M'),
        ('F', 'F'),
    )

    sort = forms.ChoiceField(choices=SORTING_CHOICES, label="Trier par")
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nom'}), label="", required=False)
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Prénom'}), label="", required=False)
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nom/Prénom'}), label="", required=False)
    building = forms.ChoiceField(choices=BUILDING_CHOICES, label="Batiment")
    room = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Chambre'}), label="", required=False)
    lot = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Lot'}), label="", required=False)
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES, label="Paiement")
    renovation = forms.ModelChoiceField(queryset=Renovation.objects.all(), label="Renovation", required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Sexe")
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="Ecole", required=False)
    empty_rooms_only = forms.BooleanField(initial=False, label="Chambres vides seules", required=False)
    exclude_temporary = forms.BooleanField(initial=False, label="Exclure les locataires passager", required=False)
    exclude_empty_rooms = forms.BooleanField(initial=False, label="Exclure les chambres vides", required=False)

class CreateTenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ('pillow', 'pillowcase', 'sheet', 'waterproof_undersheet', 'leaving', 'date_of_departure', 'blanket')
        widgets = {
            'date_of_entry': DatePicker(),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = "__all__"
        widgets = {
            'date_of_entry': DatePicker(),
            'date_of_departure': DatePicker(),
        }

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ('actualTenant', 'nextTenant')

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

class LeasingForm(forms.ModelForm):
    class Meta:
        model = Leasing
        fields = "__all__"

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('date_of_departure',)
        widgets = {
            'date_of_departure': DatePicker()
        }
