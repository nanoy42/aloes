"""Views of aloes app."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from lock_tokens.exceptions import AlreadyLockedError
from lock_tokens.sessions import (check_for_session, lock_for_session,
                                  unlock_for_session)

from documents.models import Document

from .acl import SuperuserRequiredMixin, admin_required, superuser_required
from .form import ChangePasswordForm, HomeTextEditForm, LoginForm
from .models import GeneralPreferences
from .utils import ImprovedCreateView, ImprovedDeleteView, ImprovedUpdateView


def home(request):
    """
    Displays the home page

    **Context**

    :template:`home.html`
    """
    general_preferences, _ = GeneralPreferences.objects.get_or_create()
    home_text = general_preferences.home_text
    english_home_text = general_preferences.english_home_text
    documents = Document.objects.all()
    return render(
        request,
        "home.html",
        {
            'home_text': home_text,
            'english_home_text': english_home_text,
            'documents': documents,
            'active': 'home'
        }
    )

def about(request):
    """Display about page."""
    return render(request, "about.html", {"active": "about"})

@admin_required
def edit_home_text(request):
    """Display form to edit home text (french and english)."""
    text, _ = GeneralPreferences.objects.get_or_create()
    try:
        lock_for_session(text, request.session)
    except AlreadyLockedError:
        messages.error(request, "Impossible de modifier le texte : il est en modification.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    form = HomeTextEditForm(request.POST or None, instance=text)
    if form.is_valid():
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

def login_view(request):
    """Display a form to login a user."""
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenue " + user.username)
            return redirect(request.GET.get('next', '/'))
        messages.error(request, "Nom d'utilisateur et/ou mot de passe incorrect")
    return render(request, 'form.html', {
        "form": form,
        "form_title": "Connexion",
        "form_icon": "sign-in-alt",
        "form_button": "Se connecter",
        "cancel": False
    })

@login_required
def logout_view(request):
    """Logout the user."""
    logout(request)
    messages.success(request, "Vous avez bien été déconnecté")
    return redirect(reverse('home'))

@login_required
def profile(request):
    """Display profile of the logged user."""
    form = ChangePasswordForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data['next_password'] != form.cleaned_data['next_password_repeat']:
            messages.error(request, "Les mots de passes ne correspondent pas")
        else:
            if(authenticate(
                    username=request.user.username,
                    password=form.cleaned_data['current_password']) is None):
                messages.error(request, "Le mot de passe actuel est incorrect")
            else:
                request.user.set_password(form.cleaned_data['next_password'])
                request.user.save()
                messages.success(
                    request,
                    "Le mot de passe a bien été changé. Vous pouvez dès à \
                        present vous reconnecter avec votre nouveau mot de passe"
                )
                logout(request)
                return redirect(reverse('home'))
    return render(request, "profil.html", {"form": form})

@superuser_required
def index_accounts(request):
    """List all users."""
    users = User.objects.all()
    return render(request, "index_accounts.html", {"users": users})

class UserCreate(SuperuserRequiredMixin, ImprovedCreateView): # pylint: disable=too-many-ancestors
    """Generic class to create a user."""
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = "form.html"
    success_url = reverse_lazy('indexAccounts')
    success_message = "Le compte a bien été créé.\
         Par défaut le mot de passe est le nom d'utilisateur."
    context = {
        "form_title": "Création d'un nouveau compte",
        "form_icon": "star",
        "form_button": "Créer le compte",
        "active": "accounts",
    }

    def form_valid(self, form):
        instance = form.save()
        instance.set_password(self.object.username)
        instance.is_staff = True
        instance.save()
        messages.success(self.request, self.success_message)
        return super(UserCreate, self).form_valid(form)

class UserEdit(SuperuserRequiredMixin, ImprovedUpdateView): # pylint: disable=too-many-ancestors
    """Display a form to edit a user."""
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

class UserDelete(SuperuserRequiredMixin, ImprovedDeleteView): # pylint: disable=too-many-ancestors
    """Display a confirm form to delete a user."""
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
def reset_password(request, pk):
    """Reset password to initial value (same as username)."""
    user = get_object_or_404(User, pk=pk)
    user.set_password(user.username)
    user.save()
    messages.success(request, "Le mot de passe a bien été réinitialisé.\
         Il est identique au nom d'utilisateur")
    return redirect(reverse('indexAccounts'))

@superuser_required
def admin_rights(request, pk):
    """View to give admin rights to the user with primary key pk."""
    user = get_object_or_404(User, pk=pk)
    user.is_superuser = True
    user.save()
    messages.success(request, "L'utilisateur vient de récuperer les droits administrateurs")
    return redirect(reverse('indexAccounts'))
