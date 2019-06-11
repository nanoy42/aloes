"""Forms of gestion app."""
from dal import autocomplete
import json
from django import forms

from aloes.widgets import DatePicker

from .models import Leasing, Renovation, Room, School, Tenant


class SearchForm(forms.Form):
    """Search form wich is displayed in sidebar."""
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
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Nom'}),
        label="",
        required=False
    )
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Prénom'}),
        label="",
        required=False
    )
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Nom/Prénom'}),
        label="",
        required=False
    )
    observations = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Observations'}),
        label="",
        required=False
    )
    building = forms.ChoiceField(choices=BUILDING_CHOICES, label="Bâtiment")
    room = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Chambre'}),
        label="",
        required=False
    )
    lot = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Lot'}),
        label="",
        required=False
    )
    renovation = forms.ModelChoiceField(
        queryset=Renovation.objects.all(),
        label="Renovation",
        required=False
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Sexe")
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="Ecole", required=False)
    empty_rooms_only = forms.BooleanField(
        initial=False,
        label="Chambres vides seules",
        required=False
    )
    exclude_temporary = forms.BooleanField(
        initial=False,
        label="Exclure les locataires passagers",
        required=False
    )
    exclude_empty_rooms = forms.BooleanField(
        initial=False,
        label="Exclure les chambres vides",
        required=False
    )

class CreateTenantForm(forms.ModelForm):
    """A form to create a tenant"""
    required_css_class = 'required'
    class Meta:
        model = Tenant
        fields = [
            'name',
            'first_name',
            'gender',
            'school',
            'school_year',
            'date_of_entry',
            'observations',
            'temporary',
            'cellphone',
            'birthday',
            'birthcity',
            'birthdepartement',
            'birthcountry',
            'street_number',
            'street',
            'zipcode',
            'city',
            'country',
            'email',
            'phone'
        ]
        widgets = {
            'date_of_entry': DatePicker(),
            'birthday': DatePicker(),
        }

class TenantForm(forms.ModelForm):
    """Form to edit a tenant."""
    class Meta:
        model = Tenant
        fields = [
            'name',
            'first_name',
            'gender',
            'school',
            'school_year',
            'date_of_entry',
            'observations',
            'temporary',
            'cellphone',
            'birthday',
            'birthcity',
            'birthdepartement',
            'birthcountry',
            'street_number',
            'street',
            'zipcode',
            'city', 
            'country',
            'email',
            'phone',
            'date_of_departure',
            'pillow',
            'pillowcase',
            'sheet',
            'waterproof_undersheet',
            'leaving',
            'blanket',
        ]
        widgets = {
            'date_of_entry': DatePicker(),
            'date_of_departure': DatePicker(),
            'birthday': DatePicker(),
        }


class RoomForm(forms.ModelForm):
    """Class to create and edit a room."""
    class Meta:
        model = Room
        fields = [
            'lot',
            'room',
            'rent_type',
            'renovation',
            'observations',
            'map',
        ]

class LeasingForm(forms.ModelForm):
    """Class to edit a leasing."""
    class Meta:
        model = Leasing
        fields = [
            "bail",
            "apl",
            "payment",
            "rib",
            "insuranceDeadline",
            "contract_signed",
            "contract_date",
            "caution_rib",
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
            "date_of_departure",
            "photo",
            "internal_rules_signed",
            "school_certificate",
            "debit_authorization",
        ]
        widgets = {
            'date_of_entry': DatePicker(),
            'date_of_departure': DatePicker(),
            'contract_date': DatePicker(),
            'insuranceDeadline': DatePicker(),
            'apl': DatePicker(),
        }

class LeaveForm(forms.ModelForm):
    """Form to choose a date of departure when tenant leaving."""
    class Meta:
        model = Tenant
        fields = ('date_of_departure',)
        widgets = {
            'date_of_departure': DatePicker()
        }

class DateForm(forms.Form):
    """A generic dateform."""
    date = forms.DateField(widget=DatePicker(), required=True)

class SelectTenantWNRForm(forms.Form):
    """Select a tenant without next room with autocomplete."""
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        label="Locataire",
        widget=autocomplete.ModelSelect2(url='gestion:tenantWNRAutocomplete')
    )

class SelectRoomWNTForm(forms.Form):
    """Select a room without next tenant with autocomplete."""
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=True,
        label="Chambre",
        widget=autocomplete.ModelSelect2(url='gestion:noNextTenantRoomAutocomplete')
    )

class TenantMoveInDirectForm(forms.Form):
    """Select an empty room for tenant to move in."""
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=True,
        label="Chambre",
        widget=autocomplete.ModelSelect2(url='gestion:emptyRoomAutocomplete')
    )
    date = forms.DateField(widget=DatePicker(), required=True)

class RoomMoveInDirectForm(forms.Form):
    """Select a tenant withj no room to move in."""
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        label="Locataire",
        widget=autocomplete.ModelSelect2(url='gestion:tenantWithoutRoomAutocomplete')
    )
    date = forms.DateField(widget=DatePicker(), required=True)

class ImportTenantForm(forms.Form):
    """Load json data to create a tenant."""
    jsonfield = forms.CharField(max_length=32768, label="Données JSON")

    def clean_jsonfield(self):
        """Clean field"""
        jdata = self.cleaned_data['jsonfield']
        try:
            json_data = json.loads(jdata)
            return json_data
        except:
           raise forms.ValidationError("Invalid data in jsonfield")
            