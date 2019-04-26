from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from gestion.models import Tenant, Leasing
from .utils import ODTGenerator

from datetime import datetime

def apl_infos(request, pk):
    """
    pk : primary key of a leasing
    """
    leasing = get_object_or_404(Leasing, pk=pk)
    template = ODTGenerator('generate_docs/apl_infos.odt', 'apl_infos_' + leasing.tenant.first_name + leasing.tenant.name + '.odt')
    return template.render({'leasing': leasing})

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

def lease_attestation(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(tenant.has_room):
        leasing = get_object_or_404(Leasing, tenant=tenant, room=tenant.room)
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


