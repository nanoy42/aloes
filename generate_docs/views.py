from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from gestion.models import Tenant, Leasing
from .utils import ODTGenerator

from datetime import datetime

from aloes.acl import admin_required

@admin_required
def apl_infos(request, pk):
    """
    pk : primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    template = ODTGenerator('generate_docs/apl_infos.odt', 'apl_infos_' + leasing.tenant.first_name + leasing.tenant.name + '.odt')
    return template.render({'leasing': leasing})

@admin_required
def rent_contract(request, pk):
    """
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
    if room.building == "G":
        template = ODTGenerator('generate_docs/rent_contract_aloes2.odt', 'contrat_location_' + leasing.tenant.first_name + leasing.tenant.name + '_aloes2.odt')
    else:
        template = ODTGenerator('generate_docs/rent_contract_aloes1.odt', 'contrat_location_' + leasing.tenant.first_name + leasing.tenant.name + '_aloes1.odt')
    return template.render({'leasing': leasing, 'tenant': tenant, 'gender': gender, 'born_accorded': born_accorded, 'room': room})

@admin_required
def civil_status(request, pk):
    """
    pk : primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    tenant = leasing.tenant
    room = leasing.room
    total_cheque = room.rentType.rent + room.rentType.total_rent + room.rentType.application_fee
    template = ODTGenerator('generate_docs/civil_status.odt', 'etat_civil' + leasing.tenant.first_name + leasing.tenant.name + '.odt')
    return template.render({'leasing': leasing, 'tenant': tenant, 'room': room, 'total_cheque': total_cheque})

@admin_required
def guarantee(request,pk):
    """
    pk : a primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    room = leasing.room
    tenant = leasing.tenant
    if room.building == "G":
        address = "2 rue Édouard Belin"
    else:
        address = "4 place Édouard Branly"
    template = ODTGenerator('generate_docs/guarantee.odt', 'engagement_caution_' + leasing.tenant.first_name + leasing.tenant.name + '.odt')
    return template.render({'leasing': leasing, 'room': room, 'address': address, 'total_rent': room.rentType.total_rent, 'total_rent_48': room.rentType.total_rent * 48, 'tenant': tenant})

@admin_required
def insurance_expiration(request, pk):
    """
    pk : a primary key of a leasing
    """
    tenant = get_object_or_404(Leasing, pk=pk).tenant
    template = ODTGenerator('generate_docs/insurance_expiration.odt', 'expiration_assurance_' + tenant.first_name + tenant.name + '.odt')
    return template.render({'tenant': tenant, 'now': datetime.now()})

@admin_required
def lease_end_attestation(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(tenant.date_of_departure):
        template = ODTGenerator('generate_docs/lease_end_attestation.odt', 'attestationFinDeBail' + tenant.first_name + tenant.name + '.odt')
        if(tenant.gender == "F"):
            gender = "Mme."
            born_accorded = "née"
        else:
            gender = "M."
            born_accorded = "né"
        return template.render({'now':datetime.now(), 'tenant': tenant, 'user': request.user, 'born_accorded': born_accorded, 'gender': gender})
    else:
        messages.error(request, "Impossible de générer le document : le locataire n'a pas fini son bail.")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))

@admin_required
def lease_attestation(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(tenant.current_leasing):
        leasing = tenant.current_leasing
        if(tenant.gender == "F"):
            gender = "Mme."
            born_accorded = "née"
        else:
            gender = "M."
            born_accorded = "né"
        template = ODTGenerator('generate_docs/lease_attestation.odt', 'attesationResidence' + tenant.first_name + tenant.name + '.odt')
        return template.render({'now': datetime.now(), 'tenant': tenant, 'user': request.user, 'born_accorded': born_accorded, 'gender': gender, 'leasing': leasing})
    else:
        messages.error(request, "Impossible de générer le document : le locataire n'a pas de chambre.")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))

@admin_required
def lease_attestation_english(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(tenant.current_leasing):
        leasing = tenant.current_leasing
        if(tenant.gender == "F"):
            gender = "Mme."
            born_accorded = "née"
        else:
            gender = "M."
            born_accorded = "né"
        template = ODTGenerator('generate_docs/lease_attestation_english.odt', 'attesationResidence' + tenant.first_name + tenant.name + '.odt')
        return template.render({'now': datetime.now(), 'tenant': tenant, 'user': request.user, 'born_accorded': born_accorded, 'gender': gender, 'leasing': leasing})
    else:
        messages.error(request, "Impossible de générer le document : le locataire n'a pas de chambre.")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': pk}))

@admin_required
def tenant_record(request, pk):
    leasing = get_object_or_404(Leasing, pk=pk)
    tenant = leasing.tenant
    room = leasing.room
    template = ODTGenerator('generate_docs/tenant_record.odt', 'fiche_locataire_' + tenant.first_name + tenant.name + '.odt')
    return template.render({'leasing': leasing, 'tenant': tenant, 'room': room, 'now': datetime.now()})


@admin_required
def reservation_attestation(request, pk):
    """
    pk : Primary key of a user
    """
    tenant = get_object_or_404(Tenant, pk=pk)
    if not tenant.next_leasing:
        messages.error(request, "Le locataire n'a pas réservé de chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': tenant.pk}))
    template = ODTGenerator('generate_docs/reservation_attestation.odt', 'attestation_reservation_' + tenant.first_name + tenant.name + '.odt')
    return template.render({'tenant': tenant, 'now': datetime.now()})