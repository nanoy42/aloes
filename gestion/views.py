from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import Renovation, Tenant, Leasing, School, Rent, Room
from .form import SearchForm, CreateTenantForm, RoomForm, LeasingForm, TenantForm, CreateRoomForm, LeaveForm, MoveInForm


def gestionIndex(request):
    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        res = Room.objects
        if(search_form.cleaned_data['last_name']):
            res = res.filter(actualTenant__name__icontains=search_form.cleaned_data['last_name'])
        if(search_form.cleaned_data['first_name']):
            res = res.filter(actualTenant__first_name__icontains=search_form.cleaned_data['first_name'])
        if(search_form.cleaned_data['name']):
            res = res.filter(Q(actualTenant_last_name__icontains=search_form.cleaned_data['name']) | Q(actualTenant__first_name__icontains=search_form.cleaned_data['name']))
        if(search_form.cleaned_data['room']):
            res = res.filter(room=search_form.cleaned_data['room'])
        if(search_form.cleaned_data['lot']):
            res = res.filter(lot=search_form.cleaned_data['lot'])
        if(search_form.cleaned_data['payment'] != "I"):
            res = res
        if(search_form.cleaned_data['gender'] != "I"):
            res = res.filter(actualTenant__gender=search_form.cleaned_data['gender'])
        if(search_form.cleaned_data['school']):
            res = res.filter(actualTenant__school=search_form.cleaned_data['school'])
        if(search_form.cleaned_data['empty_rooms_only']):
            res = res.filter(actualTenant=None)
        if(search_form.cleaned_data['exclude_temporary']):
            res = res.filter(actualTenant__temporary=False)
        if(search_form.cleaned_data['exclude_empty_rooms']):
            res = res.exclude(actualTenant=None)
        if(search_form.cleaned_data['building'] != "I"):
            res = filter(lambda room: room.building == search_form.cleaned_data['building'], res.all())
        else:
            res = res.all()
    else:
        res = Room.objects.all()
    return render(request, "gestion/gestionIndex.html", {"search_form": search_form, "sidebar": True, "active":"default", "rooms": res})

########## Renovations ##########

def renovationIndex(request):
    search_form = SearchForm()
    renovations = Renovation.objects.all()
    return render(request, "gestion/renovations_index.html", {"renovations": renovations, "sidebar":True, "search_form":search_form, "active":"renovations"})

class RenovationCreate(CreateView):
    model = Renovation
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexRenovation')

    class Meta:
        labels = {
            'name': 'Nom ou niveau',
            'color': 'Couleur :'
        }

    def form_valid(self, form):
        messages.success(self.request, "Le niveau de rénovation a bien été créé")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'un nouveau niveau de rénovation"
        context['form_icon'] = "star"
        context['form_button'] = "Créer le niveau de rénovation"
        context['color'] = True
        context['active'] = 'renovations'
        return context

class RenovationEdit(UpdateView):
    model = Renovation
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexRenovation')

    def form_valid(self, form):
        messages.success(self.request, "Le niveau de rénovation a bien été modifié")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Modification d'un niveau de rénovation"
        context['form_icon'] = "pencil-alt"
        context['form_button'] = "Modifier le niveau de rénovation"
        context['color'] = True
        context['active'] = 'renovations'
        return context

class RenovationDelete(DeleteView):
    model = Renovation
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexRenovation')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Le niveau de rénovation a bien été supprimé")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_title'] = "Suppression d'un niveau de rénovation"
        context['delete_object'] = "le niveau de rénovation"
        context['delete_link'] = "gestion:indexRenovation"
        context['active'] = 'renovations'
        return context

########## Schools ##########

def schoolIndex(request):
    search_form = SearchForm()
    schools = School.objects.all()
    return render(request, "gestion/schools_index.html", {"schools": schools, "sidebar":True, "search_form":search_form, "active":"schools"})

class SchoolCreate(CreateView):
    model = School
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexSchool')

    class Meta:
        labels = {
            'name': 'Nom de l\'école'
        }

    def form_valid(self, form):
        messages.success(self.request, "L'école a bien été créée")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'une nouvelle école"
        context['form_icon'] = "star"
        context['form_button'] = "Créer l'école"
        context['color'] = True
        context['active'] = 'schools'
        return context

class SchoolEdit(UpdateView):
    model = School
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexSchool')

    def form_valid(self, form):
        messages.success(self.request, "L'école a bien été modifiée")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Modification d'une école"
        context['form_icon'] = "pencil-alt"
        context['form_button'] = "Modifier l'école"
        context['color'] = True
        context['active'] = 'schools'
        return context

class SchoolDelete(DeleteView):
    model = School
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexSchool')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "L'école a bien été supprimée")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_title'] = "Suppression d'une école"
        context['delete_object'] = "l'école"
        context['delete_link'] = "gestion:indexSchool"
        context['active'] = 'schools'
        return context

########## Rents ##########

def rentIndex(request):
    search_form = SearchForm()
    rents = Rent.objects.all()
    return render(request, "gestion/rents_index.html", {"rents": rents, "sidebar":True, "search_form":search_form, "active":"rents"})

class RentCreate(CreateView):
    model = Rent
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexRent')

    class Meta:
        labels = {
            'type': 'Nom du loyer',
            'rent': 'Loyer',
        }

    def form_valid(self, form):
        messages.success(self.request, "Le loyer a bien été créé")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'un nouveau loyer"
        context['form_icon'] = "star"
        context['form_button'] = "Créer le loyer"
        context['color'] = True
        context['active'] = 'rents'
        return context

class RentEdit(UpdateView):
    model = Rent
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexRent')

    def form_valid(self, form):
        messages.success(self.request, "Le loyer a bien été modifié")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Modification d'un loyer"
        context['form_icon'] = "pencil-alt"
        context['form_button'] = "Modifier le loyer"
        context['color'] = True
        context['active'] = 'rents'
        return context

class RentDelete(DeleteView):
    model = Rent
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexRent')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Le loyer a bien été supprimé")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_title'] = "Suppression d'un loyer"
        context['delete_object'] = "le loyer"
        context['delete_link'] = "gestion:indexRent"
        context['active'] = 'rents'
        return context

########## Rooms ##########

def roomProfile(request, pk):
    search_form = SearchForm()
    room = get_object_or_404(Room, pk=pk)
    roomForm = RoomForm(request.POST or None, instance=room)
    leasings = Leasing.objects.filter(room=room)
    if(roomForm.is_valid()):
        roomForm.save()
        messages.success(request, "Les modifications ont bien été enregistrées")
    return render(request, "gestion/roomProfile.html", {"sidebar": True, "room": room, "search_form": search_form, "roomForm": roomForm, "leasings": leasings})

class RoomCreate(CreateView):
    form_class = CreateRoomForm
    template_name = "form.html"

    def get_success_url(self, **kwargs):
        return reverse("gestion:roomProfile", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "La chambre a bien été créée")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'une nouvelle chambre"
        context['form_icon'] = "star"
        context['form_button'] = "Créer la chambre"
        return context


########## Tenants ##########

def tenantProfile(request, pk):
    search_form = SearchForm()
    tenant = get_object_or_404(Tenant, pk=pk)
    tenantForm = TenantForm(request.POST or None, instance=tenant)
    previousRooms = Leasing.objects.filter(tenant=tenant)
    if(tenantForm.is_valid()):
        tenantForm.save()
        messages.success(request, "Les modifications ont été enregistrées")
    return render(request, "gestion/tenantProfile.html", {"sidebar": True, "tenant": tenant, "tenantForm": tenantForm, "search_form": search_form, "previousRooms":previousRooms})

class TenantCreate(CreateView):
    form_class = CreateTenantForm
    template_name = "form.html"

    def get_success_url(self, **kwargs):
        return reverse("gestion:tenantProfile", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Le locataire a bien été créé")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'un nouveau locataire"
        context['form_icon'] = "star"
        context['form_button'] = "Créer le locataire"
        return context


########## Leasings ##########

def leasingProfile(request, pk):
    search_form = SearchForm()
    leasing = get_object_or_404(Leasing, pk=pk)
    leasingForm = LeasingForm(request.POST or None, instance=leasing)
    if(leasingForm.is_valid()):
        leasingForm.save()
        messages.success(request, "Les modifications ont bien été enregistrées")
    return render(request, "gestion/leasingProfile.html", {"sidebar": True, "leasing": leasing, "leasingForm": leasingForm, "search_form": search_form})


########## Actions ##########

def addOneYear(request):
    tenants = Tenant.objects.all()
    for tenant in tenants:
        tenant.school_year += 1
        tenant.save()
    messages.success(request, "Tous les locataires ont été augmentés d'une année")
    next_url = request.GET.get('next', reverse('home'))
    return redirect(next_url)

def leave(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(tenant.date_of_departure):
        messages.error(request, "Le locataire a déjà quitté la résidence")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk":tenant.pk}))
    leaveForm = LeaveForm(request.POST or None, instance=tenant)
    message = "Vous vous apprêtez à faire quitter de la résidence " + str(tenant) + ". Pour continuer, indiquer la date officielle de départ de la résidence"
    if(leaveForm.is_valid()):
        leaveForm.save()
        if(tenant.has_room):
            leasing = get_object_or_404(Leasing, tenant = tenant, room = tenant.room)
            leasing.date_of_departure = leaveForm.cleaned_data['date_of_departure']
            leasing.save()
            room = tenant.room
            room.actualTenant = None
            room.save()
        messages.success(request, "Le locataire a bien quitté la résidence")
        return redirect(reverse("gestion:tenantProfile", kwargs={"pk": tenant.pk}))
    return render(request, "form.html", {"form":leaveForm, "p":message, "form_title":"Faire quitter la résidence", "form_button":"Faire quitter la résidence", "form_icon":"sign-out-alt"})

def moveIn(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(not tenant.has_next_room):
        messages.error(request, "Ce locataire n'a pas de prochaine chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    elif(tenant.nextRoom.actualTenant is not None):
        messages.error(request, "La prochaine chambre n'est pas vide")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    elif(tenant.has_room):
        messages.error(request, "Ce locataire possède actuellement une chambre. Déménagez le ou utiliser la fonction emménagement-déménagement")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk":tenant.pk}))
    moveInForm = MoveInForm(request.POST or None)
    message = "Veuillez indiquer la date d'entrée officielle dans la chambre " + str(tenant.nextRoom) + " pour " + str(tenant)
    if(moveInForm.is_valid()):
        room = tenant.nextRoom
        room.actualTenant = tenant
        room.nextTenant = None
        room.save()
        leasing = Leasing(room=room, tenant=tenant, date_of_entry=moveInForm.cleaned_data['date'])
        leasing.save()
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': tenant.pk}))
    return render(request, "form.html", {"form": moveInForm, "p": message, "form_title": "Emménagement d'un locataire", "form_button": "Emménager", "form_icon": "sign-in-alt"})
