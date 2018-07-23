from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages

import os

from .models import Document


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

    def form_valid(self, form):
        messages.success(self.request, "Le document a bien été modifié")
        if(form.has_changed() and "document" in form.changed_data):
            os.remove(self.get_object().document.path)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Modification d'un document"
        context['form_icon'] = "pencil-alt"
        context['form_button'] = "Modifier le document"
        context['file'] = True
        context['active'] = "documents"
        return context


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
