"""Urls of generate_docs app."""
from django.urls import path

from . import views

app_name = "generate_docs"

urlpatterns = [
    path('aplInfos/<int:pk>', views.apl_infos, name="aplInfos"),
    path('rentContract/<int:pk>', views.rent_contract, name="rentContract"),
    path('civilStatus/<int:pk>', views.civil_status, name="civilStatus"),
    path('guarantee/<int:pk>', views.guarantee, name="guarantee"),
    path('insuranceExpiration/<int:pk>', views.insurance_expiration, name="insuranceExpiration"),
    path('leaseEndAttestation/<int:pk>', views.lease_end_attestation, name="leaseEndAttestation"),
    path('leaseAttestation/<int:pk>', views.lease_attestation, name="leaseAttestation"),
    path(
        'leaseAttestationEnglish/<int:pk>',
        views.lease_attestation_english,
        name="leaseAttestationEnglish"
    ),
    path('tenantRecord/<int:pk>', views.tenant_record, name="tenantRecord"),
    path(
        'reservationAttestation/<int:pk>',
        views.reservation_attestation,
        name="reservationAttestation"
    ),
    path('mailingLabels', views.mailing_labels, name="mailingLabels")
]
