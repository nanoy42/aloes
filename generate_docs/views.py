from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from gestion.models import Tenant, Leasing
from .utils import ODTGenerator

from datetime import datetime

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


