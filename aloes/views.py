from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import ModelFormMixin

from documents.models import Document
from .models import GeneralPreferences
from .form import LoginForm, ChangePasswordForm, HomeTextEditForm


def home(request):
    """
    Displays the home page

    **Context**

    :template:`home.html`
    """
    homeText = GeneralPreferences.objects.get_or_create()[0].homeText
    documents = Document.objects.all()
    return render(request, "home.html", {'homeText':homeText, 'documents':documents, "active": "home"})

def about(request):
    return render(request, "about.html", {"active": "about"})

def homeTextEdit(request):
    text, _ = GeneralPreferences.objects.get_or_create()
    form = HomeTextEditForm(request.POST or None, instance = text)
    if(form.is_valid()):
        messages.success(request, "Le texte d'accueil a bien été modifié")
        form.save()
        return redirect(reverse('documents:index'))
    return render(request, "form.html", {
        "form": form,
        "form_title": "Modification du texte d'accueil",
        "form_button": "Modifier",
        "form_icon": "pencil-alt"
    })

def loginView(request):
    form = LoginForm(request.POST or None)
    if(form.is_valid()):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        if(user is not None):
            login(request, user)
            messages.success(request, "Bienvenue " + user.username)
            return redirect(reverse('home'))
        else:
            messages.error(request, "Nom d'utilisateur et/ou mot de passe incorrect")
    return render(request, 'form.html', {
        "form": form,
        "form_title": "Connexion",
        "form_icon": "sign-in-alt",
        "form_button": "Se connecter"
    })

def logoutView(request):
    logout(request)
    messages.success(request, "Vous avez bien été déconnecté")
    return redirect(reverse('home'))

def profile(request):
    form = ChangePasswordForm(request.POST or None)
    if(form.is_valid()):
        if(form.cleaned_data['next_password'] != form.cleaned_data['next_password_repeat']):
            messages.error(request, "Les mots de passes ne correspondent pas")
        else:
            if(authenticate(username = request.user.username, password = form.cleaned_data['current_password']) is None):
                messages.error(request, "Le mot de passe actuel est incorrect")
            else:
                request.user.set_password(form.cleaned_data['next_password'])
                request.user.save()
                messages.success(request, "Le mot de passe a bien été changé. Vous pouvez dès à present vous reconnecter avec votre nouveau mot de passe")
                logout(request)
                return redirect(reverse('home'))
    return render(request, "profil.html", {"form": form})

def indexAccounts(request):
    users = User.objects.all()
    return render(request, "index_accounts.html", {"users": users})

class UserCreate(CreateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = "form.html"
    success_url = reverse_lazy('indexAccounts')

    def form_valid(self, form):
        self.object = form.save()
        self.object.set_password(self.object.username)
        self.object.save()
        messages.success(self.request, "Le compte a bien été créé. Par défaut le mot de passe est le nom d'utilisateur")
        return super(ModelFormMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'un nouveau compte"
        context['form_icon'] = "star"
        context['form_button'] = "Créer le compte"
        context['active'] = 'accounts'
        return context

class UserEdit(UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = "form.html"
    success_url = reverse_lazy('indexAccounts')

    def form_valid(self, form):
        messages.success(self.request, "Le compte a bien été modifié")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Modification d'un compte"
        context['form_icon'] = "pencil-alt"
        context['form_button'] = "Modifier le compte"
        context['active'] = 'accounts'
        return context

class UserDelete(DeleteView):
    model = User
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('indexAccounts')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Le compte a bien été supprimé")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_title'] = "Suppression d'un compte"
        context['delete_object'] = "le compte"
        context['delete_link'] = "indexAccounts"
        context['active'] = 'accounts'
        return context

def resetPassword(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.set_password(user.username)
    user.save()
    messages.success(request, "Le mot de passe a bien été réinitialisé. Il est identique au nom d'utilisateur")
    return redirect(reverse('indexAccounts'))

def adminRights(request,pk):
    user = get_object_or_404(User, pk=pk)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    messages.success(request, "L'utilisateur vient de récuperer les droits administrateurs")
    return redirect(reverse('indexAccounts'))
