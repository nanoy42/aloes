from django.urls import path
from . import views

app_name = "generate_docs"

urlpatterns = [
    path('leaseEndAttestation/<int:pk>', views.lease_end_attestation, name="leaseEndAttestation"),
    path('leaseAttestation/<int:pk>', views.lease_attestation, name="leaseAttestation"),
]
