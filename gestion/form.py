from django import forms
from dal import autocomplete

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

    GENDER_CHOICES = (
        ('I', 'M/F'),
        ('M', 'M'),
        ('F', 'F'),
    )

    sort = forms.ChoiceField(choices=SORTING_CHOICES, label="Trier par")
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nom'}), label="", required=False)
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Prénom'}), label="", required=False)
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nom/Prénom'}), label="", required=False)
    building = forms.ChoiceField(choices=BUILDING_CHOICES, label="Bâtiment")
    room = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Chambre'}), label="", required=False)
    lot = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Lot'}), label="", required=False)
    renovation = forms.ModelChoiceField(queryset=Renovation.objects.all(), label="Renovation", required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Sexe")
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="Ecole", required=False)
    empty_rooms_only = forms.BooleanField(initial=False, label="Chambres vides seules", required=False)
    exclude_temporary = forms.BooleanField(initial=False, label="Exclure les locataires passagers", required=False)
    exclude_empty_rooms = forms.BooleanField(initial=False, label="Exclure les chambres vides", required=False)

class CreateTenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ('pillow', 'pillowcase', 'sheet', 'waterproof_undersheet', 'leaving', 'date_of_departure', 'blanket', 'current_leasing', 'next_leasing')
        widgets = {
            'date_of_entry': DatePicker(),
            'birthday': DatePicker(),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ('current_leasing', 'next_leasing')
        widgets = {
            'date_of_entry': DatePicker(),
            'date_of_departure': DatePicker(),
            'birthday': DatePicker(),
        }

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ('current_leasing', 'next_leasing')

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ('current_leasing', 'next_leasing')

class LeasingForm(forms.ModelForm):
    class Meta:
        model = Leasing
        fields = [
            "bail",
            "apl",
            "payment",
            "rib",
            "insuranceDeadline",
            "contractSigned",
            "contractDate", 
            "cautionRib",
            "idgarant",
            "payinslip",
            "tax_notice",
            "stranger",
            "caf",
            "residence_certificate",
            "check_guarantee",
            "guarantee",
            "issue",
            "missing_documents",
            "date_of_entry",
            "date_of_departure"
        ]
        widgets = {
            'date_of_entry': DatePicker(),
            'date_of_departure': DatePicker(),
            'contractDate': DatePicker(),
            'insuranceDeadline': DatePicker(),
            'apl': DatePicker(),
        }

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('date_of_departure',)
        widgets = {
            'date_of_departure': DatePicker()
        }

class DateForm(forms.Form):
    date = forms.DateField(widget=DatePicker(), required=True)

class selectTenantWNRForm(forms.Form):
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.has_no_next_room(), required=True, label="Locataire", widget=autocomplete.ModelSelect2(url='gestion:tenantWNRAutocomplete'))

class selectRoomWNTForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.filter(next_leasing=None), required=True, label="Chambre")

class tenantMoveInDirectForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.filter(current_leasing=None), required=True, label="Chambre", widget=autocomplete.ModelSelect2(url='gestion:emptyRoomAutocomplete'))
    date = forms.DateField(widget=DatePicker(), required=True)

class roomMoveInDirectForm(forms.Form):
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.has_no_room(), required=True, label="Locataire", widget=autocomplete.ModelSelect2(url='gestion:tenantWithoutRoomAutocomplete'))
    date = forms.DateField(widget=DatePicker(), required=True)
