"""Views of documents app."""
import os

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from aloes.acl import AdminRequiredMixin, admin_required
from aloes.utils import (ImprovedCreateView, ImprovedDeleteView,
                         LockableUpdateView)

from .models import Document


class DocumentIndex(AdminRequiredMixin, ListView): # pylint: disable=too-many-ancestors
    """Generic class based view to list all documents."""
    model = Document
    context_object_name = "documents"
    template_name = "documents/documents_index.html"
    queryset = Document.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = "documents"
        return context

class DocumentCreate(AdminRequiredMixin, ImprovedCreateView): # pylint: disable=too-many-ancestors
    """Class based view to create a document."""
    model = Document
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('documents:index')
    success_message = "Le document a bien été créé"
    context = {
        "form_title": "Création d'un nouveau document",
        "form_icon": "star",
        "form_button": "Créer le document",
        "file": True,
        "active": "documents"
    }

class DocumentEdit(AdminRequiredMixin, LockableUpdateView): # pylint: disable=too-many-ancestors
    """Class based view to edit a document."""
    model = Document
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('documents:index')
    success_message = "Le document a bien été modifié"
    lock_message = "Impossible de modifier le document : il est en cours de modification"
    context = {
        "form_title": "Modification d'un document",
        "form_icon": "pencil-alt",
        "form_button": "Modifier",
        "active": "documents",
        "file": True
    }

    def form_valid(self, form):
        if self.get_object().document:
            os.remove(self.get_object().document.path)
        if self.get_object().english_document:
            os.remove(self.get_object().english_document.path)
        return super().form_valid(form)

class DocumentDelete(AdminRequiredMixin, ImprovedDeleteView): # pylint: disable=too-many-ancestors
    """Class based view to delete a document."""
    model = Document
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('documents:index')
    success_message = "Le document a bien été supprimé"
    context = {
        "delete_title": "Suppression d'un document",
        "delete_object": "le document",
        "delete_link": "documents:index",
        "active": "documents"
    }

    def delete(self, request, *args, **kwargs):
        if self.get_object().document:
            os.remove(self.get_object().document.path)
        if self.get_object().english_document:
            os.remove(self.get_object().english_document.path)
        return super().delete(request, *args, **kwargs)

@admin_required
def document_switch_active(request, pk):
    """Change active status of document wiith primary key pk."""
    document = get_object_or_404(Document, pk=pk)
    document.active = 1 - document.active
    document.save()
    return redirect(reverse('documents:index'))
