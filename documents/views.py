from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from lock_tokens.exceptions import AlreadyLockedError
from lock_tokens.sessions import check_for_session, lock_for_session, unlock_for_session


import os

from .models import Document
from .forms import DocumentForm
from aloes.acl import admin_required, superuser_required, AdminRequiredMixin, SuperuserRequiredMixin
from django.contrib.auth.decorators import login_required
from aloes.utils import ImprovedCreateView, ImprovedUpdateView, ImprovedDeleteView, LockableUpdateView


class DocumentIndex(ListView, AdminRequiredMixin):
    model = Document
    context_object_name = "documents"
    template_name = "documents/documents_index.html"
    queryset = Document.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = "documents"
        return context

class DocumentCreate(ImprovedCreateView, AdminRequiredMixin):
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

class DocumentEdit(LockableUpdateView, AdminRequiredMixin):
    model = Document
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('documents:index')
    success_message = "Le document a bien été modifié"
    lock_message = "Impossible de modifier le document : il est en cours de modification"
    context = {"form_title": "Modification d'un document", "form_icon": "pencil-alt", "form_button": "Modifier", "active": "documents", "file": True}

class DocumentDelete(ImprovedDeleteView, AdminRequiredMixin):
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
        os.remove(self.get_object().document.path)
        return super().delete(request, *args, **kwargs)

@admin_required
def DocumentSwitchActive(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.active = 1 - document.active
    document.save()
    return redirect(reverse('documents:index'))
