from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import ModelFormMixin
from lock_tokens.exceptions import AlreadyLockedError
from lock_tokens.sessions import check_for_session, lock_for_session, unlock_for_session

from documents.models import Document
from .models import GeneralPreferences
from .form import LoginForm, ChangePasswordForm, HomeTextEditForm
from .acl import admin_required, superuser_required, AdminRequiredMixin, SuperuserRequiredMixin
from django.contrib.auth.decorators import login_required
from .utils import ImprovedCreateView, ImprovedUpdateView, ImprovedDeleteView

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

@admin_required
def homeTextEdit(request):
    text, _ = GeneralPreferences.objects.get_or_create()
    try:
        lock_for_session(text, request.session)
    except AlreadyLockedError:
        messages.error(request, "Impossible de modifier le texte : il est en modification.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    form = HomeTextEditForm(request.POST or None, instance = text)
    if(form.is_valid()):
        if not check_for_session(text, request.session):
            messages.error(request, "Impossible de modifier le texte : il est en modification.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        messages.success(request, "Le texte d'accueil a bien été modifié")
        form.save()
        unlock_for_session(text, request.session)
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
        "form_button": "Se connecter",
        "cancel": False
    })

@login_required
def logoutView(request):
    logout(request)
    messages.success(request, "Vous avez bien été déconnecté")
    return redirect(reverse('home'))

@login_required
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

@superuser_required
def indexAccounts(request):
    users = User.objects.all()
    return render(request, "index_accounts.html", {"users": users})

class UserCreate(ImprovedCreateView, SuperuserRequiredMixin):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = "form.html"
    success_url = reverse_lazy('indexAccounts')
    success_message = "Le compte a bien été créé. Par défaut le mot de passe est le nom d'utilisateur."
    context = {
        "form_title": "Création d'un nouveau compte",
        "form_icon": "star",
        "form_button": "Créer le compte",
        "active": "accounts",
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.set_password(self.object.username)
        self.object.is_staff = True
        self.object.save()
        messages.success(self.request, self.success_message)
        return super(ModelFormMixin, self).form_valid(form)

class UserEdit(ImprovedUpdateView, SuperuserRequiredMixin):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = "form.html"
    success_url = reverse_lazy('indexAccounts')
    success_message = "Le compte a bien été modifié"
    context = {
        "form_title": "Modification d'un compte",
        "form_icon": "pencil-alt",
        "form_button": "Modifier le compte",
        "active": "accounts",
    }

class UserDelete(ImprovedDeleteView, SuperuserRequiredMixin):
    model = User
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('indexAccounts')
    success_message = "Le compte a bien été supprimé"
    context = {
        "delete_title": "Suppression d'un compte",
        "delete_object": "le compte",
        "delete_link": "indexAccounts",
        "active": "accounts",
    }

@superuser_required
def resetPassword(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.set_password(user.username)
    user.save()
    messages.success(request, "Le mot de passe a bien été réinitialisé. Il est identique au nom d'utilisateur")
    return redirect(reverse('indexAccounts'))

@superuser_required
def adminRights(request,pk):
    user = get_object_or_404(User, pk=pk)
    user.is_superuser = True
    user.save()
    messages.success(request, "L'utilisateur vient de récuperer les droits administrateurs")
    return redirect(reverse('indexAccounts'))
