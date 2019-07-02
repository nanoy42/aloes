"""Views of generate_docs app."""
from datetime import datetime
import csv

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from aloes.acl import admin_required
from gestion.models import Leasing, Tenant

from .forms import MailingLabelForm
from .utils import ODTGenerator


@admin_required
def apl_infos(request, pk):
    """
    Render apl_infos.odt.

    pk : primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    template = ODTGenerator(
        'generate_docs/apl_infos.odt',
        ('apl_infos_' + leasing.tenant.first_name + leasing.tenant.name + '.odt').replace(" ", "")
    )
    return template.render({'leasing': leasing})

@admin_required
def rent_contract(request, pk):
    """
    Render rent_contrat_aloes1.odt or rent_contract_aloes2.odt.

    pk : primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    room = leasing.room
    tenant = leasing.tenant
    if leasing.tenant.gender == "M":
        gender = "M."
        born_accorded = "né"
    else:
        gender = "Mme."
        born_accorded = "née"
    floor = str(room)[1]
    if floor == "1":
        floor += "er étage"
    else:
        floor += "ieme étage"
    if room.building == "G":
        template = ODTGenerator(
            'generate_docs/rent_contract_aloes2.odt',
            ('contrat_location_' + leasing.tenant.first_name + leasing.tenant.name + '_aloes2.odt').replace(" ", "")
        )
    else:
        template = ODTGenerator(
            'generate_docs/rent_contract_aloes1.odt',
            ('contrat_location_' + leasing.tenant.first_name + leasing.tenant.name + '_aloes1.odt').replace(" ", "")
        )
    return template.render({
        'leasing': leasing,
        'tenant': tenant,
        'gender': gender,
        'born_accorded': born_accorded,
        'room': room,
        'floor': floor
    })

@admin_required
def civil_status(request, pk):
    """
    Render civil_status.odt.

    pk : primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    tenant = leasing.tenant
    room = leasing.room
    total_cheque = room.rent_type.rent + room.rent_type.total_rent + room.rent_type.application_fee
    template = ODTGenerator(
        'generate_docs/civil_status.odt',
        ('etat_civil' + leasing.tenant.first_name + leasing.tenant.name + '.odt').replace(" ", "")
    )
    return template.render({
        'leasing': leasing,
        'tenant': tenant,
        'room': room,
        'total_cheque': total_cheque
    })

@admin_required
def guarantee(request, pk):
    """
    Render guarantee.odt.

    pk : a primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    room = leasing.room
    tenant = leasing.tenant
    if room.building == "G":
        address = "2 rue Édouard Belin"
    else:
        address = "4 place Édouard Branly"
    template = ODTGenerator(
        'generate_docs/guarantee.odt',
        ('engagement_caution_' + leasing.tenant.first_name + leasing.tenant.name + '.odt').replace(" ", "")
    )
    return template.render({
        'leasing': leasing,
        'room': room,
        'address': address,
        'total_rent': room.rent_type.total_rent,
        'total_rent_48': room.rent_type.total_rent * 48,
        'tenant': tenant
    })

@admin_required
def insurance_expiration(request, pk):
    """
    Render insurance_expiration.odt.

    pk : a primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    tenant = leasing.tenant
    template = ODTGenerator(
        'generate_docs/insurance_expiration.odt',
        ('expiration_assurance_' + tenant.first_name + tenant.name + '.odt').replace(" ", "")
    )
    return template.render({
        'leasing': leasing,
        'tenant': tenant,
        'now': datetime.now(),
        'user': request.user
    })

@admin_required
def lease_end_attestation(request, pk):
    """
    Render lease_end_attestation.odt

    pk : primary key of a tenant
    """
    tenant = get_object_or_404(Tenant, pk=pk)
    if tenant.date_of_departure:
        template = ODTGenerator(
            'generate_docs/lease_end_attestation.odt',
            ('attestationFinDeBail' + tenant.first_name + tenant.name + '.odt').replace(" ", "")
        )
        if tenant.gender == "F":
            gender = "Mme."
            born_accorded = "née"
        else:
            gender = "M."
            born_accorded = "né"
        return template.render({
            'now':datetime.now(),
            'tenant': tenant,
            'user': request.user,
            'born_accorded': born_accorded,
            'gender': gender
        })
    messages.error(
        request,
        "Impossible de générer le document : le locataire n'a pas fini son bail."
    )
    return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))

@admin_required
def lease_attestation(request, pk):
    """
    Render lease_attestion.odt

    pk : primary key of a tenant
    """
    tenant = get_object_or_404(Tenant, pk=pk)
    if tenant.current_leasing:
        leasing = tenant.current_leasing
        if tenant.gender == "F":
            gender = "Mme."
            born_accorded = "née"
        else:
            gender = "M."
            born_accorded = "né"
        template = ODTGenerator(
            'generate_docs/lease_attestation.odt',
            ('attesationResidence' + tenant.first_name + tenant.name + '.odt').replace(" ", "")
        )
        return template.render({
            'now': datetime.now(),
            'tenant': tenant,
            'user': request.user,
            'born_accorded': born_accorded,
            'gender': gender,
            'leasing': leasing
        })
    messages.error(request, "Impossible de générer le document : le locataire n'a pas de chambre.")
    return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))

@admin_required
def lease_attestation_english(request, pk):
    """
    Render lease_attestation_english.odt

    pk :primary key of a tenant
    """
    tenant = get_object_or_404(Tenant, pk=pk)
    if tenant.current_leasing:
        leasing = tenant.current_leasing
        if tenant.gender == "F":
            gender = "Mme."
            born_accorded = "née"
        else:
            gender = "M."
            born_accorded = "né"
        template = ODTGenerator(
            'generate_docs/lease_attestation_english.odt',
            ('attesationResidence' + tenant.first_name + tenant.name + '.odt').replace(" ", "")
        )
        return template.render({
            'now': datetime.now(),
            'tenant': tenant,
            'user': request.user,
            'born_accorded': born_accorded,
            'gender': gender,
            'leasing': leasing
        })
    messages.error(request, "Impossible de générer le document : le locataire n'a pas de chambre.")
    return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))

@admin_required
def tenant_record(request, pk):
    """
    Render tenant_record.odt

    pk : primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    tenant = leasing.tenant
    room = leasing.room
    template = ODTGenerator(
        'generate_docs/tenant_record.odt',
        ('fiche_locataire_' + tenant.first_name + tenant.name + '.odt').replace(" ", "")
    )
    return template.render({
        'leasing': leasing,
        'tenant': tenant,
        'room': room,
        'now': datetime.now()
    })


@admin_required
def reservation_attestation(request, pk):
    """
    Render reservation_attestation.odt

    pk : Primary key of a user
    """
    tenant = get_object_or_404(Tenant, pk=pk)
    if not tenant.next_leasing:
        messages.error(request, "Le locataire n'a pas réservé de chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': tenant.pk}))
    template = ODTGenerator(
        'generate_docs/reservation_attestation.odt',
        ('attestation_reservation_' + tenant.first_name + tenant.name + '.odt').replace(" ", "")
    )
    return template.render({'tenant': tenant, 'now': datetime.now(), 'user': request.user})

@admin_required
def mailing_labels(request):
    """
    Generates mailing labels from a csv file

    Correct form of csv: 
        first column : Name of tenant
        second column : Room
    """
    form = MailingLabelForm(request.POST or None, request.FILES or None)
    if 'cancel' in request.POST:
        messages.success(request, "Demande annulée")
        return redirect(request.POST.get('cancel') or "home")
    if form.is_valid():
        csv_reader = csv.reader(request.FILES['file'].read().decode("utf8").split('\n'))
        tenant_doubles = pair(csv_reader)
        template = ODTGenerator(
            'generate_docs/mailing_labels.odt',
            'etiquettes_courrier.odt'
        )
        return template.render({'tenant_doubles': tenant_doubles})
    return render(request, "form.html", {
        "form_title": "Génération des étiquettes de courrier",
        "form_icon": "envelope",
        "form_button": "Générer",
        "form": form,
        "file": True,
    })

def pair(iterator):
    """
    Group by two elements of the iterator
    """
    try:
        while True:
            a = next(iterator)
            b = next(iterator, None)
            print(a)
            print(b)
            yield a, b
    except StopIteration:
        return
