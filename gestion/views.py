"""Views of gestion app.""" # pylint: disable=too-many-lines
import csv
import os

from dal import autocomplete
from django.contrib import messages
from django.core import management
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django_cron import CronJobBase, Schedule
from lock_tokens.exceptions import AlreadyLockedError
from lock_tokens.sessions import (check_for_session, lock_for_session,
                                  unlock_for_session)

from aloes.acl import AdminRequiredMixin, admin_required
from aloes.utils import (ImprovedCreateView, ImprovedDeleteView,
                         LockableUpdateView)

from .form import (CreateTenantForm, DateForm, LeasingForm,
                   LeaveForm, RoomForm, SearchForm, TenantForm,
                   RoomMoveInDirectForm, SelectRoomWNTForm,
                   SelectTenantWNRForm, TenantMoveInDirectForm,
                   ImportTenantForm)
from .models import Leasing, Map, Renovation, Rent, Room, School, Tenant

from django.db import connection


@admin_required
def gestion_index(request):  # pylint : disable=too-many-branches
    """Main page of gestion app."""
    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        res = Room.objects.select_related('current_leasing').select_related('next_leasing').select_related('renovation').select_related('rent_type')
        if search_form.cleaned_data['last_name']:
            res = res.filter(
                current_leasing__tenant__name__icontains=\
                    search_form.cleaned_data['last_name'])
        if search_form.cleaned_data['first_name']:
            res = res.filter(
                current_leasing__tenant__first_name__icontains=\
                    search_form.cleaned_data['first_name'])
        if search_form.cleaned_data['name']:
            res = res.filter(Q(current_leasing__tenant__name__icontains=\
                search_form.cleaned_data['name']) | Q(
                    current_leasing__tenant__first_name__icontains=search_form.cleaned_data['name']))
        if search_form.cleaned_data['room']:
            res = res.filter(
                room__istartswith=search_form.cleaned_data['room'])
        if search_form.cleaned_data['lot']:
            res = res.filter(lot=search_form.cleaned_data['lot'])
        if search_form.cleaned_data['gender'] != "I":
            res = res.filter(
                current_leasing__tenant__gender=search_form.cleaned_data['gender'])
        if search_form.cleaned_data['school']:
            res = res.filter(
                current_leasing__tenant__school=search_form.cleaned_data['school'])
        if search_form.cleaned_data['empty_rooms_only']:
            res = res.filter(current_leasing__tenant=None)
        if search_form.cleaned_data['exclude_temporary']:
            res = res.filter(current_leasing__tenant__temporary=False)
        if search_form.cleaned_data['exclude_empty_rooms']:
            res = res.exclude(current_leasing__tenant=None)
        if search_form.cleaned_data['renovation']:
            res = res.filter(renovation=search_form.cleaned_data['renovation'])
        if search_form.cleaned_data['building'] != "I":
            res = res.filter(
                room__istartswith=search_form.cleaned_data['building'])
        if search_form.cleaned_data['sort']:
            if search_form.cleaned_data['sort'] == "room":
                res = res.order_by("room")
            if search_form.cleaned_data['sort'] == "first_name":
                res = res.order_by("current_leasing__tenant__first_name")
            if search_form.cleaned_data['sort'] == "last_name":
                res = res.order_by("current_leasing__tenant__name")
    else:
        res = Room.objects.filter(is_active=True).select_related('current_leasing').select_related('next_leasing').select_related('renovation').select_related('rent_type')
    return render(
        request,
        "gestion/gestion_index.html",
        {
            "search_form": search_form,
            "sidebar": True,
            "active": "default",
            "rooms": res
        }
    )

########## Renovations ##########

@admin_required
def renovations_index(request):
    """List of all renovation levels."""
    search_form = SearchForm()
    renovations = Renovation.objects.all()
    return render(
        request,
        "gestion/renovations_index.html",
        {
            "renovations": renovations,
            "sidebar": True,
            "search_form": search_form,
            "active": "renovations"
        }
    )


class RenovationCreate(AdminRequiredMixin, ImprovedCreateView): # pylint: disable=too-many-ancestors
    """Class based view to create a renovation level."""
    model = Renovation
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexRenovation')
    success_message = "Le niveau de rénovation a bien été créé"
    context = {
        "form_title": "Création d'un nouveau niveau de rénovation",
        "form_icon": "star",
        "form_button": "Créer le niveau de rénovation",
        "color": True,
        "active": "renovations",
    }

    class Meta:
        """Meta information"""
        labels = {
            'name': 'Nom ou niveau',
            'color': 'Couleur :'
        }


class RenovationEdit(AdminRequiredMixin, LockableUpdateView): # pylint: disable=too-many-ancestors
    """Class based view to edit a renovation level."""
    model = Renovation
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy("gestion:indexRenovation")
    success_message = "Le niveau de rénovation a bien été modifié"
    lock_message = "Impossible de modifier le niveau de rénovation :\
                    il est en cours de modification"
    context = {
        "form_title": "Modification d'un niveau de rénovation",
        "form_icon": "pencil-alt",
        "form_button": "Modifier",
        "color": True,
        "active": "renovations"}


class RenovationDelete(AdminRequiredMixin, ImprovedDeleteView): # pylint: disable=too-many-ancestors
    """Class based view to confirm suppression a renovation level."""
    model = Renovation
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexRenovation')
    success_message = "Le niveau de rénovation a bien été supprimé"
    context = {
        "delete_title": "Supression d'un niveau de rénovation",
        "delete_object": "le niveau de rénovation",
        "delete_link": "gestion:indexRenovation",
        "active": "renovations"
    }

########## Schools ##########

@admin_required
def schools_index(request):
    """List all schools."""
    search_form = SearchForm()
    schools = School.objects.all()
    return render(request,
                  "gestion/schools_index.html",
                  {"schools": schools,
                   "sidebar": True,
                   "search_form": search_form,
                   "active": "schools"})


class SchoolCreate(AdminRequiredMixin, ImprovedCreateView): # pylint: disable=too-many-ancestors
    """Class based view to create a school."""
    model = School
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexSchool')
    success_message = "L'école a bien été créée"
    context = {
        "form_title": "Création d'une nouvelle école",
        "form_icon": "star",
        "form_button": "Créer l'école",
        "active": "schools",
    }

    class Meta:
        """Meta information."""
        labels = {
            'name': 'Nom de l\'école'
        }


class SchoolEdit(AdminRequiredMixin, LockableUpdateView): # pylint: disable=too-many-ancestors
    """Class based view to edit a school."""
    model = School
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexSchool')
    success_message = "L'école a bien été modifiée"
    lock_message = "Impossible de modifier l'école : elle est en cours de modification"
    context = {
        "form_title": "Modification d'une école",
        "form_icon": "pencil-alt",
        "form_button": "Modifier",
        "active": "schools"}


class SchoolDelete(AdminRequiredMixin, ImprovedDeleteView): # pylint: disable=too-many-ancestors
    """Class based view to confirm the suppression of a school."""
    model = School
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexSchool')
    success_message = "L'école a bien été supprimée"
    context = {
        "delete_title": "Suppression d'une école",
        "delete_object": "l'école",
        "delete_link": "gestion:indexSchool",
        "active": "schools"
    }

########## Rents ##########


@admin_required
def rents_index(request):
    """List all rents."""
    search_form = SearchForm()
    rents = Rent.objects.all()
    return render(
        request,
        "gestion/rents_index.html",
        {
            "rents": rents,
            "sidebar": True,
            "search_form": search_form,
            "active": "rents"
        }
    )

class RentCreate(AdminRequiredMixin, ImprovedCreateView): # pylint: disable=too-many-ancestors
    """Class based view to create a rent."""
    model = Rent
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexRent')
    success_message = "Le loyer a bien été créé"
    context = {
        "form_title": "Création d'un nouveau loyer",
        "form_icon": "star",
        "form_button": "Créer le loyer",
        "active": "rents"
    }

    class Meta:
        """Meta information."""
        labels = {
            'type': 'Nom du loyer',
            'rent': 'Loyer',
        }


class RentEdit(AdminRequiredMixin, LockableUpdateView): # pylint: disable=too-many-ancestors
    """Class based view to edit a rent."""
    model = Rent
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexRent')
    success_message = "Le loyer a bien été modifié"
    lock_message = "Impossible de modifier le loyer : il est en cours de modification"
    context = {
        "form_title": "Modification d'un loyer",
        "form_icon": "pencil-alt",
        "form_button": "Modifier",
        "active": "rents"}


class RentDelete(AdminRequiredMixin, ImprovedDeleteView): # pylint: disable=too-many-ancestors
    """Class based view to confirm the suppression of a rent."""
    model = Rent
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexRent')
    success_message = "Le loyer a bien été supprimé"
    context = {
        "delete_title": "Suppresion d'un loyer",
        "delete_object": "le loyer",
        "delete_link": "gestion:indexRent",
        "active": "rents"
    }

########## Rooms ##########


@admin_required
def room_profile(request, pk):
    """Display room profile."""
    search_form = SearchForm()
    room = get_object_or_404(Room, pk=pk)
    return render(
        request,
        "gestion/room_profile.html",
        {
            "sidebar": True,
            "room": room,
            "search_form": search_form
        }
    )


@admin_required
def edit_room(request, pk):
    """
    Display a form to edit a room

    pk : primary key of a room
    """
    search_form = SearchForm()
    room = get_object_or_404(Room, pk=pk)
    try:
        lock_for_session(room, request.session)
    except AlreadyLockedError:
        messages.error(
            request,
            "Impossible de modifier la chambre : elle est en cours de modification."
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))
    room_form = RoomForm(request.POST or None, instance=room)
    if 'cancel' in request.POST:
        messages.success(request, "Demande annulée")
        unlock_for_session(room, request.session)
        return redirect(request.POST.get('cancel') or "home")
    if room_form.is_valid():
        if not check_for_session(room, request.session):
            messages.error(
                request,
                "Impossible de modifier la chambre : elle est en cours de modification."
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))
        room_form.save()
        messages.success(
            request, "Les modifications ont bien été enregistrées")
        unlock_for_session(room, request.session)
        return redirect(reverse('gestion:roomProfile', kwargs={'pk': room.pk}))
    return render(
        request,
        "gestion/edit_room.html",
        {
            "sidebar": True,
            "room": room,
            "search_form": search_form,
            "roomForm": room_form
        }
    )


class RoomCreate(AdminRequiredMixin, ImprovedCreateView): # pylint: disable=too-many-ancestors
    """Class based view to create Room."""
    form_class = RoomForm
    template_name = "form.html"
    success_message = "La chambre a bien été créée"
    context = {
        "form_title": "Création d'une nouvelle chambre",
        "form_icon": "star",
        "form_button": "Créer la chambre"
    }

    def get_success_url(self):
        return reverse("gestion:roomProfile", kwargs={'pk': self.object.pk})


@admin_required
def add_next_tenant(request, pk):
    """Add next leasing to a room (next leasing)."""
    room = get_object_or_404(Room, pk=pk)
    if room.next_leasing:
        messages.error(request, "Cette chambre est déjà reservée")
        return redirect(reverse('gestion:roomProfile', kwargs={'pk': pk}))
    form = SelectTenantWNRForm(request.POST or None)
    if form.is_valid():
        if 'cancel' in request.POST:
            messages.success(request, "Demande annulée")
            return redirect(request.POST.get('cancel') or "home")
        tenant = form.cleaned_data['tenant']
        if tenant.next_leasing:
            messages.error(request, "Ce locataire a déjà reservé une chambre")
        else:
            leasing = Leasing(room=room, tenant=tenant)
            leasing.save()
            room.next_leasing = leasing
            room.save()
            tenant.next_leasing = leasing
            tenant.save()
            messages.success(request, "La chambre a bien été réservée")
        return redirect(reverse('gestion:roomProfile', kwargs={'pk': pk}))
    message = "Choisir un locataire pour réserver la chambre"
    return render(
        request,
        "form.html",
        {
            "form": form,
            "form_title": "Réservation de la chambre " + str(room),
            "p": message,
            "form_button": "Réserver la chambre",
            "form_icon": "star"
        }
    )


@admin_required
def room_move_in_direct(request, pk):
    """
    Form to select a tenant with no room and move it to room

    pk : primary key of the room
    """
    room = get_object_or_404(Room, pk=pk)
    if room.current_tenant:
        messages.error(request, "La chambre n'est pas vide")
        return redirect(reverse('gestion:roomProfile', kwargs={"pk": pk}))
    form = RoomMoveInDirectForm(request.POST or None)
    if form.is_valid():
        if 'cancel' in request.POST:
            messages.success(request, "Demande annulée")
            return redirect(request.POST.get('cancel') or "home")
        tenant = form.cleaned_data['tenant']
        if tenant.room:
            messages.error(request, "Ce locataire possède déjà une chambre")
        else:
            leasing = Leasing(
                room=room,
                tenant=tenant,
                date_of_entry=form.cleaned_data['date'])
            leasing.save()
            room.current_leasing = leasing
            room.save()
            tenant.current_leasing = leasing
            tenant.save()
            messages.success(request, "Le locataire a bien été emménagé")
        return redirect(reverse('gestion:roomProfile', kwargs={"pk": pk}))
    message = "Choisir un locataire et la date d'entrée dans la chambre"
    return render(
        request,
        "form.html",
        {
            "form": form,
            "form_title": "Location de la chambre " + str(room),
            "p": message,
            "form_button": "Attribuer",
            "form_icon": "sign-in-alt"
        }
    )


class ChangeRoomMap(AdminRequiredMixin, LockableUpdateView):
    """Class based view to change map of a room."""
    model = Room
    fields = ("map",)
    template_name = "form.html"
    success_message = "Le plan a bien été modifié"
    lock_message = "Impossible de modifier le plan : il est en cours de modification"
    context = {
        "form_title": "Modification d'un plan",
        "form_icon": "pencil-alt",
        "form_button": "Modifier",
        "active": "rooms",
        "file": True
    }

    def form_valid(self, form):
        if self.get_object().map:
            os.remove(self.get_object().map.path)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("gestion:roomProfile", kwargs={'pk': self.object.pk})

def room_switch_activate(request, pk):
    """Invert the active status of a room"""
    room = get_object_or_404(Room, pk=pk)
    room.is_active = 1 - room.is_active
    room.save()
    messages.success(request, "Le statut a bien été changé.")
    return redirect(reverse('gestion:roomProfile', kwargs={'pk': pk}))


@admin_required
def inactive_rooms(request):
    """Display inactive rooms."""
    rooms = Room.objects.filter(is_active=False)
    return render(
        request,
        "gestion/inactive_rooms.html",
        {
            "rooms": rooms
        }
    )

########## Tenants ##########

@admin_required
def tenant_profile(request, pk):
    """
    Display profile of a tenant

    pk : primary key of a tenant
    """
    search_form = SearchForm()
    tenant = get_object_or_404(Tenant, pk=pk)
    return render(
        request,
        "gestion/tenant_profile.html",
        {
            "sidebar": True,
            "tenant": tenant,
            "search_form": search_form
        }
    )


@admin_required
def edit_tenant(request, pk):
    """
    Display a form to edit a tenant

    pk : primary key of a tenant
    """
    search_form = SearchForm()
    tenant = get_object_or_404(Tenant, pk=pk)
    try:
        lock_for_session(tenant, request.session)
    except AlreadyLockedError:
        messages.error(
            request,
            "Impossible de modifier le locataire : il est en cours de modification."
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))
    tenant_form = TenantForm(request.POST or None, instance=tenant)
    if 'cancel' in request.POST:
        messages.success(request, "Demande annulée")
        unlock_for_session(tenant, request.session)
        return redirect(request.POST.get('cancel') or "home")
    if tenant_form.is_valid():
        if not check_for_session(tenant, request.session):
            messages.error(
                request,
                "Impossible de modifier le locataire : il est en cours de modification."
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))
        tenant_form.save()
        messages.success(request, "Les modifications ont été enregistrées")
        unlock_for_session(tenant, request.session)
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': tenant.pk}))
    return render(
        request,
        "gestion/edit_tenant.html",
        {
            "sidebar": True,
            "tenant": tenant,
            "tenantForm": tenant_form,
            "search_form": search_form
        }
    )


class TenantCreate(AdminRequiredMixin, ImprovedCreateView): # pylint: disable=too-many-ancestors
    """Class based view to create a tenant."""
    form_class = CreateTenantForm
    template_name = "form.html"
    success_message = "Le locataire a bien été créé"
    context = {
        "form_title": "Création d'un nouveau locataire",
        "form_icon": "star",
        "form_button": "Créer le locataire"
    }

    def get_success_url(self):
        return reverse("gestion:tenantProfile", kwargs={'pk': self.object.pk})

def import_tenant(request):
    """Import tenant in json format"""
    form = ImportTenantForm(request.POST or None)
    if form.is_valid():
        json_data = form.cleaned_data["jsonfield"]
        fields = json_data[0]["fields"]
        if fields["school"]:
            school = fields["school"]
        else:
            school = fields["other_school"]
        school = School.objects.filter(name=school)
        if school:
            school = school[0]
        else:
            school = None
        tenant = Tenant(
            name=fields["last_name"],
            first_name=fields["first_name"],
            gender={"H": "M", "F": "F"}[fields["gender"]],
            school=school,
            school_year=1,
            cellphone=fields["phone_number"],
            birthday=fields["birthdate"],
            birthcity=fields["birthplace"],
            birthdepartement=fields["birth_departement"],
            birthcountry=fields["birth_country"],
            street_number=fields["street"][:fields["street"].index(" ")],
            street=fields["street"][fields["street"].index(" ")+1:],
            city=fields["city"],
            zipcode=fields["zip_code"],
            email=fields["email"]
        )
        tenant.save()
        messages.success(request, "Le locataire a bien été importé. Pensez à vérifier l'école, aisni que le pays de résidence actuel.")
        return redirect(reverse("gestion:tenantProfile", kwargs={"pk": tenant.pk}))
    return render(request, "form.html", {"form": form})

@admin_required
def add_next_room(request, pk):
    """
    Add next room (next leasing) to a tenant without next room (next leasing)

    pk : primary key of a tenant
    """
    tenant = get_object_or_404(Tenant, pk=pk)
    if tenant.next_room:
        messages.error(request, "Ce locataire a déjà réservé une chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))
    form = SelectRoomWNTForm(request.POST or None)
    if form.is_valid():
        if 'cancel' in request.POST:
            messages.success(request, "Demande annulée")
            return redirect(request.POST.get('cancel') or "home")
        room = form.cleaned_data['room']
        if room.next_leasing:
            messages.error(request, "Cette chambre est déjà réservée")
        else:
            leasing = Leasing(room=room, tenant=tenant)
            leasing.save()
            room.next_leasing = leasing
            room.save()
            tenant.next_leasing = leasing
            tenant.save()
            messages.success(request, "Le locataire a bien réservé la chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))
    message = "Choisir une chambre non réservée"
    return render(
        request,
        "form.html",
        {
            "form": form,
            "form_title": "Réservation pour le locataire " + str(tenant),
            "p": message,
            "form_button": "Réserver la chambre",
            "form_icon": "star"
        }
    )


@admin_required
def tenant_move_in_direct(request, pk):
    """
    Form to select an empty room and move tenant in

    pk : primary key of a tenant
    """
    tenant = get_object_or_404(Tenant, pk=pk)
    if tenant.room:
        messages.error(request, "Ce locataire possède déjà une chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": pk}))
    form = TenantMoveInDirectForm(request.POST or None)
    if form.is_valid():
        if 'cancel' in request.POST:
            messages.success(request, "Demande annulée")
            return redirect(request.POST.get('cancel') or "home")
        room = form.cleaned_data['room']
        if room.current_leasing:
            messages.error(request, "Cette chambre n'est pas vide")
        else:
            leasing = Leasing(
                room=room,
                tenant=tenant,
                date_of_entry=form.cleaned_data['date']
            )
            leasing.save()
            room.current_leasing = leasing
            room.save()
            tenant.current_leasing = leasing
            tenant.save()
            messages.success(request, "Le locataire a bien été emménagé")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": pk}))
    message = "Choisir une chambre vide et la date d'entrée dans la chambre"
    return render(
        request,
        "form.html",
        {
            "form": form,
            "form_title": "Attribution d'une chambre à " + str(tenant),
            "p": message,
            "form_button": "Attribuer",
            "form_icon": "sign-in-alt"
        }
    )


@admin_required
def homeless_tenants(request):
    """Display tenants without room."""
    homeless = Tenant.objects.filter(current_leasing=None)
    return render(
        request,
        "gestion/homeless_tenants.html",
        {
            "homeless": homeless
        }
    )

########## Leasings ##########


@admin_required
def leasing_profile(request, pk):
    """
    Display profile of a leasing

    pk : primary key of a leasing
    """
    search_form = SearchForm()
    leasing = get_object_or_404(Leasing, pk=pk)
    return render(
        request,
        "gestion/leasing_profile.html",
        {
            "sidebar": True,
            "leasing": leasing,
            "search_form": search_form
        }
    )

@admin_required
def edit_leasing(request, pk):
    """
    Display form to edit a leasing

    pk : primary key of a leasing
    """
    search_form = SearchForm()
    leasing = get_object_or_404(Leasing, pk=pk)
    try:
        lock_for_session(leasing, request.session)
    except AlreadyLockedError:
        messages.error(
            request,
            "Impossible de modifier le dossier : il est en cours de modification."
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))
    leasing_form = LeasingForm(request.POST or None, instance=leasing)
    if 'cancel' in request.POST:
        messages.success(request, "Demande annulée")
        unlock_for_session(leasing, request.session)
        return redirect(request.POST.get('cancel') or "home")
    if leasing_form.is_valid():
        if not check_for_session(leasing, request.session):
            messages.error(
                request,
                "Impossible de modifier le dossier : il est en cours de modification.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        leasing_form.save()
        messages.success(
            request, "Les modifications ont bien été enregistrées")
        unlock_for_session(leasing, request.session)
        return redirect(reverse('gestion:leasingProfile', kwargs={'pk': leasing.pk}))
    return render(
        request,
        "gestion/edit_leasing.html",
        {
            "sidebar": True,
            "leasing": leasing,
            "leasingForm": leasing_form,
            "search_form": search_form
        }
    )

########## Actions ##########

@admin_required
def add_one_year(request):
    """Add one to school_year field of every tenant"""
    tenants = Tenant.objects.all()
    for tenant in tenants:
        tenant.school_year += 1
        tenant.save()
    messages.success(
        request,
        "Tous les locataires ont été augmentés d'une année"
    )
    next_url = request.GET.get('next', reverse('home'))
    return redirect(next_url)


@admin_required
def leave(request, pk):
    """Display a form to select date of departure and leave from leasing."""
    tenant = get_object_or_404(Tenant, pk=pk)
    if tenant.date_of_departure:
        messages.error(request, "Le locataire a déjà quitté la résidence")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    leave_form = LeaveForm(request.POST or None, instance=tenant)
    message = "Vous vous apprêtez à faire quitter de la résidence " + \
        str(tenant) + ". Pour continuer, indiquer la date officielle de départ de la résidence"
    if leave_form.is_valid():
        if 'cancel' in request.POST:
            messages.success(request, "Demande annulée")
            return redirect(request.POST.get('cancel') or "home")
        leave_form.save()
        if tenant.current_leasing:
            leasing = tenant.current_leasing
            leasing.date_of_departure = leave_form.cleaned_data['date_of_departure']
            leasing.save()
            room = tenant.room
            room.current_leasing = None
            room.save()
            tenant.current_leasing = None
            tenant.save()
        messages.success(request, "Le locataire a bien quitté la résidence")
        return redirect(reverse("gestion:tenantProfile", kwargs={"pk": tenant.pk}))
    return render(
        request,
        "form.html",
        {
            "form": leave_form,
            "p": message,
            "form_title": "Faire quitter la résidence",
            "form_button": "Faire quitter la résidence",
            "form_icon": "sign-out-alt"
        }
    )


@admin_required
def move_out(request, pk, mode):
    """Display a form to select a date of departure from the current room

    pk : primary key of a tenant
    mode : tenant or room
    """
    if mode not in ["tenant", "room"]:
        mode = "tenant"
    tenant = get_object_or_404(Tenant, pk=pk)
    if not tenant.room:
        messages.error(request, "Le locataire n'est dans aucune chambre actuellement")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    move_out_form = DateForm(request.POST or None)
    message = "Veuillez indiquer la date de sortie officielle de la chambre " + \
        str(tenant.room) + " pour " + str(tenant)
    if mode == "room":
        form_title = "Vider la chambre " + str(tenant.room)
        form_button = "Vider la chambre"
    else:
        form_title = "Déménager " + str(tenant)
        form_button = "Déménager"
    if move_out_form.is_valid():
        if 'cancel' in request.POST:
            messages.success(request, "Demande annulée")
            return redirect(request.POST.get('cancel') or "home")
        leasing = tenant.current_leasing
        leasing.date_of_departure = move_out_form.cleaned_data['date']
        leasing.save()
        room = tenant.room
        room.current_leasing = None
        room.save()
        tenant.current_leasing = None
        tenant.save()
        if mode == "room":
            messages.success(request, "La chambre a bien été vidé")
            return redirect(reverse("gestion:roomProfile", kwargs={"pk": room.pk}))
        messages.success(request, "Le locataire a bien déménagé")
        return redirect(reverse("gestion:tenantProfile", kwargs={"pk": tenant.pk}))
    return render(
        request,
        "form.html",
        {
            "form": move_out_form,
            "p": message,
            "form_title": form_title,
            "form_button": form_button,
            "form_icon": "sign-out-alt"
        }
    )


@admin_required
def move_in(request, pk, mode): # pylint: disable=too-many-return-statements
    """Display a form to select date of entry in the room

    pk : primary key of a tenant
    mode : tenant or room
    """
    if(mode not in ["tenant", "room"]):
        mode = "tenant"
    tenant = get_object_or_404(Tenant, pk=pk)
    if not tenant.next_room:
        messages.error(request, "Ce locataire n'a pas de prochaine chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    if tenant.next_leasing.room.current_leasing is not None:
        if mode == "room":
            messages.error(request, "La chambre n'est pas vide")
            return redirect(reverse('gestion:roomProfile', kwargs={"pk": tenant.next_room.pk}))
        messages.error(request, "La prochaine chambre n'est pas vide")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    if tenant.room:
        if mode == "room":
            messages.error(
                request,
                "Le prochain locataire possède actuellement\
                     une chambre. Déménager le avant de l'emménager"
            )
        else:
            messages.error(
                request,
                "Ce locataire possède actuellement une chambre. Déménagez le avant de l'emménager"
            )
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    move_in_form = DateForm(request.POST or None)
    message = "Veuillez indiquer la date d'entrée officielle dans la chambre " + \
        str(tenant.next_room) + " pour " + str(tenant)
    if move_in_form.is_valid():
        if 'cancel' in request.POST:
            messages.success(request, "Demande annulée")
            return redirect(request.POST.get('cancel') or "home")
        room = tenant.next_room
        leasing = tenant.next_leasing
        leasing.date_of_entry = move_in_form.cleaned_data['date']
        leasing.save()
        tenant.current_leasing = leasing
        tenant.next_leasing = None
        tenant.save()
        room.current_leasing = leasing
        room.next_leasing = None
        room.save()
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': tenant.pk}))
    return render(
        request,
        "form.html",
        {
            "form": move_in_form,
            "p": message,
            "form_title": "Emménagement d'un locataire",
            "form_button": "Emménager",
            "form_icon": "sign-in-alt"
        }
    )

@admin_required
def cancel_next_room(request, pk, mode):
    """Cancel next leasing

    pk : primary key of a tenant
    mode : tenant or room
    """
    if mode not in ["tenant", "room"]:
        mode = "tenant"
    tenant = get_object_or_404(Tenant, pk=pk)
    if not tenant.next_room:
        messages.error(request, "Ce locataire n'a pas de prochaine chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    leasing = tenant.next_leasing
    room = tenant.next_leasing.room
    room.next_leasing = None
    room.save()
    tenant.next_leasing = None
    tenant.save()
    leasing.delete()
    if mode == "room":
        messages.success(request, "Le prochain locataire a bien été annulé")
        return redirect(reverse('gestion:roomProfile', kwargs={"pk": room.pk}))
    messages.success(request, "La prochaine chambre a été annulée")
    return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))

########## Maps ##########


@admin_required
def map_index(request):
    """List all maps."""
    search_form = SearchForm()
    maps = Map.objects.all()
    return render(
        request,
        "gestion/maps_index.html",
        {
            "maps": maps,
            "sidebar": True,
            "search_form": search_form,
            "active": "maps"
        }
    )


class MapCreate(AdminRequiredMixin, ImprovedCreateView):  # pylint: disable=too-many-ancestors
    """Display a form to create a map."""
    model = Map
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexMap')
    success_message = "Le plan a bien été créé"
    context = {
        "form_title": "Création d'un nouveau plan",
        "form_icon": "star",
        "form_button": "Créer le plan",
        "file": True,
        "active": "maps"
    }


class MapEdit(AdminRequiredMixin, LockableUpdateView):  # pylint: disable=too-many-ancestors
    """Display a form to edit a map."""
    model = Map
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexMap')
    success_message = "Le plan a bien été modifié"
    lock_message = "Impossible de modifier le plan : il est en cours de modification"
    context = {
        "form_title": "Modification d'un plan",
        "form_icon": "pencil-alt",
        "form_button": "Modifier",
        "active": "maps",
        "file": True,
        }

    def form_valid(self, form):
        if self.get_object().map:
            os.remove(self.get_object().map.path)
        return super().form_valid(form)


class MapDelete(AdminRequiredMixin, ImprovedDeleteView):  # pylint: disable=too-many-ancestors
    """Display a confirm delete form."""
    model = Map
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexMap')
    success_message = "Le plan a bien été supprimé"
    context = {
        "delete_title": "Suppression d'un plan",
        "delete_object": "le plan",
        "delete_link": "gestion:indexMap",
        "active": "maps"
    }

    def delete(self, request, *args, **kwargs):
        if self.get_object().map:
            os.remove(self.get_object().map.path)
        return super().delete(request, *args, **kwargs)


########## Other ##########

@admin_required
def export_csv(request):
    """View to export main page information in csv."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Chambre (lot)', 'Locataire (email)',
                     'Réservation', 'Réparation', 'Loyer'])
    rooms = Room.objects.all()
    for room in rooms:
        if room.current_leasing:
            tenant_text = str(room.current_leasing.tenant) + \
                "(" + str(room.current_leasing.tenant.email) + ")"
        else:
            tenant_text = "Pas de locataire actuel"

        writer.writerow([str(room),
                         tenant_text,
                         str(room.next_leasing.tenant if room.next_leasing else "Pas réservée"),
                         str(room.renovation or "Non indiqué"),
                         str(room.rent_type or "Non indiqué")])
    tenants = Tenant.objects.filter(current_leasing=None)
    for tenant in tenants:
        writer.writerow(["Pas de chambre", str(tenant), "", "", ""])
    return response

########## autocomplete ########


class EmptyRoomAutocomplete(autocomplete.Select2QuerySetView):  # pylint: disable=too-many-ancestors
    """Autocomplete view for empty rooms."""
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Room.object.none()
        qs = Room.objects.filter(is_active=True).filter(current_leasing=None)
        if self.q:
            qs = qs.filter(room__istartswith=self.q)
        return qs


class NoNextTenantRoomAutomplete(autocomplete.Select2QuerySetView):  # pylint: disable=too-many-ancestors
    """Autocomplete view for rooms with no next tenant (next leasing)."""
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Room.object.none()
        qs = Room.objects.filter(is_active=True).filter(next_leasing=None)
        if self.q:
            qs = qs.filter(room__istartswith=self.q)
        return qs


class TenantWNRAutocomplete(autocomplete.Select2QuerySetView):  # pylint: disable=too-many-ancestors
    """Autocomplete view for tenants with no next room(next leasing)."""
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tenant.object.none()
        qs = Tenant.objects.filter(next_leasing=None)
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) |
                           Q(first_name__icontains=self.q))
        return qs


class TenantWithoutRoomAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete view for tenants without room (current leasing)."""
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tenant.objects.none()
        qs = Tenant.objects.filter(current_leasing=None)
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) |
                           Q(first_name__icontains=self.q))
        return qs


@admin_required
def mail_tenants(request):
    """Display a link to send an email to all tenants with room."""
    tenants_with_room = Tenant.objects.exclude(email__isnull=True).prefetch_related('current_leasing__room').exclude(current_leasing__isnull=True)
    buildings = ["A", "B", "C", "D", "E", "G"]
    b_emails = {}
    for building in buildings:
        tenants_in_building =  tenants_with_room.filter(current_leasing__room__room__startswith=building)
        b_emails[building] = [tenant.email for tenant in tenants_in_building]
    tenants_emails = [
        tenant.email for tenant in tenants_with_room
    ]
    return render(
        request,
        "gestion/mail_tenants.html",
        {
            "tenants_emails": tenants_emails,
            "b_emails": b_emails,
        }
    )

########## Backup ##########


def copy_backups():
    """Copy backups to external location."""
    return True


def backup(request):
    """Save bdd in JSON"""
    management.call_command('dbbackup')
    copy_backups()
    messages.success(request, "La base de données a bien été sauvegardée.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


class Backup(CronJobBase):
    """Cron class to make backup each day at 6pm."""
    RUN_AT_TIMES = ['18:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'gestion.Backup'

    def do(self): # pylint: disable=invalid-name, no-self-use
        """Call ddbakcup command and copy_backups"""
        management.call_command('dbbackup')
        copy_backups()
