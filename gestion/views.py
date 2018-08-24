from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import Renovation, Tenant, Leasing, School, Rent, Room, Map
from .form import SearchForm, CreateTenantForm, RoomForm, LeasingForm, TenantForm, CreateRoomForm, LeaveForm, DateForm, selectTenantWNRForm, selectRoomWNTForm, tenantMoveInDirectForm, roomMoveInDirectForm


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
    leasings = Leasing.objects.filter(room=room).order_by("-pk")
    if(leasings.count() > 0 and leasings[0].tenant == room.nextTenant):
        nextLeasing = leasings[0]
        if(leasings.count() > 1):
            leasings = leasings[1:]
            if(leasings[0].tenant == room.actualTenant):
                actualLeasing = leasings[0]
                if(leasings.count() > 1):
                    leasings = leasings[1:]
                else:
                    leasings = None
            else:
                actualLeasing = None
        else:
            leasings = None
            actualLeasing = None
    elif(leasings.count() > 0 and leasings[0].tenant == room.actualTenant):
        nextLeasing = None
        actualLeasing = leasings[0]
        if(leasings.count() > 1):
            leasings = leasings[1:]
        else:
            leasings = None
    else:
        nextLeasing = None
        actualLeasing = None
    if(roomForm.is_valid()):
        roomForm.save()
        messages.success(request, "Les modifications ont bien été enregistrées")
    return render(request, "gestion/roomProfile.html", {"sidebar": True, "room": room, "search_form": search_form, "roomForm": roomForm, "leasings": leasings, "nextLeasing": nextLeasing, "actualLeasing": actualLeasing})

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

def addNextTenant(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if(room.nextTenant):
        messages.error(request, "Cette chambre est déjà reservée")
        return redirect(reverse('gestion:roomProfile', kwargs={'pk':pk}))
    else:
        form = selectTenantWNRForm(request.POST or None)
        if(form.is_valid()):
            tenant = form.cleaned_data['tenant']
            if(tenant.has_next_room):
                messages.error(request, "Ce locataire a déjà reservé une chambre")
            else:
                room.nextTenant = tenant
                room.save()
                leasing = Leasing(room=room, tenant=tenant)
                leasing.save()
                messages.success(request, "La chambre a bien été réservée")
            return redirect(reverse('gestion:roomProfile', kwargs={'pk':pk}))
    message = "Choisir un locataire pour réserver la chambre"
    return render(request, "form.html", {"form": form, "form_title": "Réservation de la chambre " + str(room), "p": message, "form_button": "Réserver la chambre", "form_icon": "star"})

def roomMoveInDirect(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if(room.actualTenant):
        messages.error(request, "La chambre n'est pas vide")
        return redirect(reverse('gestion:roomProfile', kwargs={"pk":pk}))
    else:
        form = roomMoveInDirectForm(request.POST or None)
        if(form.is_valid()):
            tenant = form.cleaned_data['tenant']
            if(tenant.has_room):
                messages.error(request, "Ce locataire possède déjà une chambre")
            else:
                room.actualTenant = tenant
                room.save()
                leasing = Leasing(room=room, tenant=tenant, date_of_entry=form.cleaned_data['date'])
                leasing.save()
                messages.success(request, "Le locataire a bien été emménagé")
            return redirect(reverse('gestion:roomProfile', kwargs={"pk":pk}))
    message = "Choisir un locataire et la date d'entrée dans la chambre"
    return render(request, "form.html", {"form":form, "form_title": "Location de la chambre " + str(room), "p": message, "form_button": "Attribuer", "form_icon": "sign-in-alt"})

class ChangeRoomMap(UpdateView):
    model = Room
    fields = ("map",)
    template_name = "form.html"

    def get_success_url(self, **kwargs):
        return reverse("gestion:roomProfile", kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Le plan a bien été modifié")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Modification du plan de " + str(self.object)
        context['form_icon'] = "pencil-alt"
        context['form_button'] = "Modifier le plan"
        context['file'] = True
        context['active'] = 'rooms'
        return context



########## Tenants ##########

def tenantProfile(request, pk):
    search_form = SearchForm()
    tenant = get_object_or_404(Tenant, pk=pk)
    tenantForm = TenantForm(request.POST or None, instance=tenant)
    leasings = Leasing.objects.filter(tenant=tenant).order_by("-pk")
    if(leasings.count() > 0 and tenant.has_next_room and leasings[0].room == tenant.nextRoom):
        nextLeasing = leasings[0]
        if(leasings.count() > 1):
            leasings = leasings[1:]
            if(tenant.has_room and leasings[0] == tenant.room):
                actualLeasing = leasings[0]
                if(leasings.count() > 1):
                    leasings = leasings[1:]
                else:
                    leasings = None
            else:
                actualLeasing = None
        else:
            leasings = None
            actualLeasing = None
    elif(leasings.count() > 0 and tenant.has_room and leasings[0].room == tenant.room):
        nextLeasing = None
        actualLeasing = leasings[0]
        if(leasings.count() > 1):
            leasings = leasings[1:]
        else:
            leasings = None
    else:
        actualLeasing = None
        nextLeasing = None
    if(tenantForm.is_valid()):
        tenantForm.save()
        messages.success(request, "Les modifications ont été enregistrées")
    return render(request, "gestion/tenantProfile.html", {"sidebar": True, "tenant": tenant, "tenantForm": tenantForm, "search_form": search_form, "leasings": leasings, "actualLeasing": actualLeasing, "nextLeasing": nextLeasing})

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

def addNextRoom(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(tenant.has_next_room):
        messages.error(request, "Ce locataire a déjà réservé une chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk':pk}))
    else:
        form = selectRoomWNTForm(request.POST or None)
        if(form.is_valid()):
            room = form.cleaned_data['room']
            if(room.nextTenant):
                messages.error(request, "Cette chambre est déjà réservée")
            else:
                room.nextTenant = tenant
                room.save()
                leasing = Leasing(room=room, tenant=tenant)
                leasing.save()
                messages.success(request, "Le locataire a bien réservé la chambre")
            return redirect(reverse('gestion:tenantProfile', kwargs={'pk':pk}))
    message = "Choisir une chambre non réservée"
    return render(request, "form.html", {"form": form, "form_title": "Réservation pour le locataire " + str(tenant), "p": message, "form_button": "Réserver la chambre", "form_icon": "star"})

def tenantMoveInDirect(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if(tenant.has_room):
        messages.error(request, "Ce locataire possède déjà une chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk":pk}))
    else:
        form = tenantMoveInDirectForm(request.POST or None)
        if(form.is_valid()):
            room = form.cleaned_data['room']
            if(room.actualTenant):
                messages.error(request, "Cette chambre n'est pas vide")
            else:
                room.actualTenant = tenant
                room.save()
                leasing = Leasing(room=room, tenant=tenant, date_of_entry=form.cleaned_data['date'])
                leasing.save()
                messages.success(request, "Le locataire a bien été emménagé")
            return redirect(reverse('gestion:tenantProfile', kwargs={"pk":pk}))
    message = "Choisir une chambre vide et la date d'entrée dans la chambre"
    return render(request, "form.html", {"form":form, "form_title": "Attribution d'une chambre à " + str(tenant), "p": message, "form_button": "Attribuer", "form_icon": "sign-in-alt"})

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

def moveOut(request, pk, mode):
    if(mode not in ["tenant", "room"]):
        mode = "tenant"
    tenant = get_object_or_404(Tenant, pk=pk)
    if(not tenant.has_room):
        messages.error(request, "Le locataire n'est dans aucune chambre actuellement")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk":tenant.pk}))
    moveOutForm = DateForm(request.POST or None)
    message = "Veuillez indiquer la date de sortie officielle de la chambre " + str(tenant.room) + " pour " + str(tenant)
    if(mode == "room"):
        form_title = "Vider la chambre " + str(tenant.room)
        form_button = "Vider la chambre"
    else:
        form_title = "Déménager " + str(tenant)
        form_button = "Déménager"
    if(moveOutForm.is_valid()):
        leasing = get_object_or_404(Leasing, tenant = tenant, room = tenant.room)
        leasing.date_of_departure = moveOutForm.cleaned_data['date']
        leasing.save()
        room = tenant.room
        room.actualTenant = None
        room.save()
        if(mode == "room"):
            messages.success(request, "La chambre a bien été vidé")
            return redirect(reverse("gestion:roomProfile", kwargs={"pk":room.pk}))
        else:
            messages.success(request, "Le locataire a bien déménagé")
            return redirect(reverse("gestion:tenantProfile", kwargs={"pk": tenant.pk}))
    return render(request, "form.html", {"form": moveOutForm, "p": message, "form_title": form_title, "form_button": form_button, "form_icon": "sign-out-alt"})

def moveIn(request, pk, mode):
    if(mode not in ["tenant", "room"]):
        mode = "tenant"
    tenant = get_object_or_404(Tenant, pk=pk)
    if(not tenant.has_next_room):
        messages.error(request, "Ce locataire n'a pas de prochaine chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    elif(tenant.nextRoom.actualTenant is not None):
        if(mode == "room"):
            messages.error(request, "La chambre n'est pas vide")
            return redirect(reverse('gestion:roomProfile', kwargs={"pk":tenant.next_room.pk}))
        else:
            messages.error(request, "La prochaine chambre n'est pas vide")
            return redirect(reverse('gestion:tenantProfile', kwargs={"pk": tenant.pk}))
    elif(tenant.has_room):
        if(mode == "room"):
            messages.error(request, "Le prochain locataire possède actuellement une chambre. Déménager le avant de l'emménager")
        else:
            messages.error(request, "Ce locataire possède actuellement une chambre. Déménagez le avant de l'emménager")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk":tenant.pk}))
    moveInForm = DateForm(request.POST or None)
    message = "Veuillez indiquer la date d'entrée officielle dans la chambre " + str(tenant.nextRoom) + " pour " + str(tenant)
    if(moveInForm.is_valid()):
        room = tenant.nextRoom
        room.actualTenant = tenant
        room.nextTenant = None
        room.save()
        leasing = Leasing.objects.get(room=room, tenant=tenant)
        leasing.date_of_entry=moveInForm.cleaned_data['date']
        leasing.save()
        return redirect(reverse('gestion:tenantProfile', kwargs={'pk': tenant.pk}))
    return render(request, "form.html", {"form": moveInForm, "p": message, "form_title": "Emménagement d'un locataire", "form_button": "Emménager", "form_icon": "sign-in-alt"})

def cancelNextRoom(request, pk, mode):
    if(mode not in ["tenant", "room"]):
        mode = "tenant"
    tenant = get_object_or_404(Tenant, pk=pk)
    if(not tenant.has_next_room):
        messages.error(request, "Ce locataire n'a pas de prochaine chambre")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk":tenant.pk}))
    room = tenant.nextRoom
    room.nextTenant = None
    room.save()
    leasing = Leasing.objects.get(room=room, tenant=tenant)
    leasing.delete()
    if(mode == "room"):
        messages.success(request, "Le prochain locataire a bien été annulé")
        return redirect(reverse('gestion:roomProfile', kwargs={"pk":room.pk}))
    else:
        messages.success(request, "La prochaine chambre a été annulée")
        return redirect(reverse('gestion:tenantProfile', kwargs={"pk":room.pk}))


########## Maps ##########


def mapIndex(request):
    search_form = SearchForm()
    maps = Map.objects.all()
    return render(request, "gestion/maps_index.html", {"maps": maps, "sidebar":True, "search_form":search_form, "active":"maps"})

class MapCreate(CreateView):
    model = Map
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexMap')

    def form_valid(self, form):
        messages.success(self.request, "Le plan a bien été créé")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Création d'un nouveau plan"
        context['form_icon'] = "star"
        context['form_button'] = "Créer le plan"
        context['file'] = True
        context['active'] = 'maps'
        return context

class MapEdit(UpdateView):
    model = Map
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy('gestion:indexMap')

    def form_valid(self, form):
        messages.success(self.request, "Le plan a bien été modifié")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Modification d'un plan"
        context['form_icon'] = "pencil-alt"
        context['form_button'] = "Modifier le plan"
        context['file'] = True
        context['active'] = 'maps'
        return context

class MapDelete(DeleteView):
    model = Map
    context_object_name = "object_name"
    template_name = "delete.html"
    success_url = reverse_lazy('gestion:indexMap')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Le plan a bien été supprimé")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_title'] = "Suppression d'un plan"
        context['delete_object'] = "le plan"
        context['delete_link'] = "gestion:indexMap"
        context['active'] = 'maps'
        return context
