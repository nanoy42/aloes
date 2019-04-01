from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from lock_tokens.exceptions import AlreadyLockedError
from lock_tokens.sessions import check_for_session, lock_for_session, unlock_for_session


import os

from .models import Document
from .forms import DocumentForm


class DocumentIndex(ListView):
    model = Document
    context_object_name = "documents"
    template_name = "documents/documents_index.html"
    queryset = Document.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = "documents"
        return context

class DocumentCreate(CreateView):
    model = Document
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('documents:index')

    def form_valid(self, form):
        messages.success(self.request, "Le document a bien été créé")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'un nouveau document"
        context['form_icon'] = "star"
        context['form_button'] = "Créer le document"
        context['file'] = True
        context['active'] = "documents"
        return context

class DocumentEdit(UpdateView):
    model = Document
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('documents:index')
    success_message = "Le document a bien été modifié"
    lock_message = "Impossible de modifier le document : il est en cours de modification"
    context = {"form_title": "Modification d'un document", "form_icon": "pencil-alt", "form_button": "Modifier", "active": "documents", "file": True}

class DocumentDelete(DeleteView):
    model = Document
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('documents:index')

    def delete(self, request, *args, **kwargs):
        os.remove(self.get_object().document.path)
        messages.success(request, "Le document a bien été supprimé")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_title'] = "Suppression d'un document"
        context['delete_object'] = "le document"
        context['delete_link'] = "documents:index"
        context['active'] = "documents"
        return context

def DocumentSwitchActive(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.active = 1 - document.active
    document.save()
    return redirect(reverse('documents:index'))
