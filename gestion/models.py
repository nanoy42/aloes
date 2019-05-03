from django.db import models
from colorfield.fields import ColorField
from django.db.utils import OperationalError

class School(models.Model):
    class Meta:
        verbose_name = "Ecole"
    name = models.CharField(max_length=255, verbose_name="Nom de l'école")

    def __str__(self):
        return self.name

class Renovation(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom ou niveau")
    description = models.TextField()
    color = ColorField(default="#FF0000", verbose_name="Couleur :")

    def __str__(self):
        return self.name

class Rent(models.Model):
    class Meta:
        verbose_name="Loyer"
    type = models.TextField(max_length=255, verbose_name="Genre")
    rent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Loyer")
    service = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Forfait services")
    charges = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Charges")
    application_fee = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Frais de dossier")
    surface = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Superficie")

    def __str__(self):
        return self.type + " (" + str(self.surface) + " m2)"

    @property
    def supplements(self):
        return self.service + self.charges

    @property
    def total_rent(self):
        return self.rent + self.supplements 

class TenantManager(models.Manager):
    def has_no_next_room(self):
        try:
            ids = [tenant.id for tenant in Tenant.objects.all() if not tenant.next_room]
            return Tenant.objects.filter(id__in=ids)
        except:
            return None

    def has_no_room(self):
        try:
            ids = [tenant.id for tenant in Tenant.objects.all() if not tenant.room]
            return Tenant.objects.filter(id__in=ids)
        except:
            return None

    def has_room(self):
        try:
            ids = [tenant.id for tenant in Tenant.objects.all() if tenant.room]
            return Tenant.objects.filter(id__in=ids)
        except OperationalError:
            return None

class Tenant(models.Model):
    class Meta:
        verbose_name = "Locataire"

    GENDER_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    name = models.CharField(max_length=255, verbose_name="Nom")
    first_name = models.CharField(max_length=255, verbose_name="Prénom")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Sexe")
    school = models.ForeignKey('School', on_delete=models.PROTECT, verbose_name="Ecole")
    school_year = models.PositiveIntegerField(default=1, verbose_name="Année d'étude", blank=True, null=True)
    date_of_entry = models.DateField(verbose_name="Date d'entrée à la rez", blank=True, null=True)
    date_of_departure = models.DateField(blank=True, verbose_name="Date de sortie de la rez", null=True)
    observations = models.TextField(verbose_name="Observations", blank=True)
    temporary = models.BooleanField(default=False, verbose_name="Passager")
    cellphone = models.CharField(max_length=10, verbose_name="Numéro de téléphone portable", blank=True)
    leaving = models.BooleanField(default=False, verbose_name="Sur le départ")
    waterproof_undersheet = models.BooleanField(default=False, verbose_name="Alèse")
    pillow = models.BooleanField(default=False, verbose_name="Oreiller")
    pillowcase = models.BooleanField(default=False, verbose_name="Taie d'oreiller")
    blanket = models.BooleanField(default=False, verbose_name="Couverture")
    sheet = models.BooleanField(default=False, verbose_name="Drap")
    birthday = models.DateField(verbose_name="Date de naissance", blank=True, null=True)
    birthcity = models.CharField(max_length=255, verbose_name="Ville de naissance", blank=True)
    birthdepartement = models.CharField(max_length=255, verbose_name="Département de naissance", blank=True)
    birthcountry = models.CharField(max_length=255, verbose_name="Pays de naissance", blank=True)
    street_number = models.PositiveIntegerField(verbose_name="N° de rue", blank=True, null=True)
    street = models.CharField(max_length=255, verbose_name="Rue", blank=True)
    zipcode = models.PositiveIntegerField(verbose_name="Code postal", blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name="Ville", blank=True)
    country = models.CharField(max_length=255, verbose_name="Pays", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=10, verbose_name="Téléphone fixe", blank=True)
    current_leasing = models.ForeignKey('Leasing', on_delete=models.PROTECT, verbose_name="Dossier actuel", blank=True, null=True, related_name="current_tenants")
    next_leasing = models.ForeignKey('Leasing', on_delete=models.PROTECT, verbose_name="Dossier suivant", blank=True, null=True, related_name="next_tenants")

    objects = TenantManager()

    def __str__(self):
        if(self.gender == "M"):
            pre = "M."
        else:
            pre = "Mme."
        return pre + " " + self.first_name + " " + self.name

    @property
    def room(self):
        if self.current_leasing:
            return self.current_leasing.room
        else:
            return None

    @property
    def next_room(self):
        if self.next_leasing:
            return self.next_leasing.room
        else:
            return None

    @property
    def previous_leasings(self):
        leasings = Leasing.objects.filter(tenant=self)
        if self.current_leasing:
            leasings = leasings.exclude(pk=self.current_leasing.pk)
        if self.next_leasing:
            leasings = leasings.exclude(pk=next_leasing.pk).order_by['-pk']
        return leasings.order_by('-pk')

    @property
    def previous_rooms(self):
        pks = [leasing.room.pk for leasing in self.previous_leasings]
        return Room.objects.filter(pk__in=pks)

class Room(models.Model):
    class Meta:
        verbose_name = "Chambre"

    lot = models.PositiveIntegerField(verbose_name="Lot")
    room = models.CharField(max_length=6, verbose_name="Chambre")
    rentType = models.ForeignKey('Rent', on_delete=models.PROTECT, verbose_name="Loyer")
    renovation = models.ForeignKey('Renovation', on_delete=models.PROTECT, verbose_name="Niveau de rénovation", blank=True, null=True)
    observations = models.TextField(verbose_name="Observations", blank=True)
    map = models.ImageField(verbose_name="Plan", blank=True, null=True)
    current_leasing = models.ForeignKey('Leasing', on_delete=models.PROTECT, verbose_name="Dossier actuel", blank=True, null=True, related_name="current_rooms")
    next_leasing = models.ForeignKey('Leasing', on_delete=models.PROTECT, verbose_name="Dossier suivant", blank=True, null=True, related_name="next_rooms")

    def __str__(self):
        return self.room

    def building(self):
        return self.room[0]

    @property
    def current_tenant(self):
        if self.current_leasing:
            return self.current_leasing.tenant
        else:
            return None

    @property
    def next_tenant(self):
        if self.next_leasing:
            return self.next_leasing.tenant
        else:
            return Leasing

    @property
    def previous_leasings(self):
        leasings = Leasing.objects.filter(room=self)
        if self.current_leasing:
            leasings = leasings.exclude(pk=self.current_leasing.pk)
        if self.next_leasing:
            leasings = leasings.exclude(pk=next_leasing.pk).order_by['-pk']
        return leasings.order_by('-pk')

    @property
    def previous_tenants(self):
        pks = [leasing.tenant.pk for leasing in self.previous_leasings]
        return Tenant.objects.filter(pk__in=pks)


class Leasing(models.Model):
    class Meta:
        verbose_name="Location"

    PAYMENT_CHOICES = (
        ('direct_debit', 'Prélèvement'),
        ('bank_transfer', 'Virement'),
        ('check', 'Chèque'),
        ('cash', 'Espèces'),
        ('special', 'Special'),
    )
    tenant = models.ForeignKey('Tenant', on_delete=models.PROTECT, verbose_name="Locataire")
    room = models.ForeignKey('Room', on_delete=models.PROTECT, verbose_name="Chambre")
    bail = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Caution", blank=True, null=True)
    apl = models.DateField(verbose_name="APL", blank=True, null=True)
    payment = models.CharField(max_length=255, verbose_name="Paiement", choices=PAYMENT_CHOICES, blank=True)
    rib = models.BooleanField(default=False, verbose_name="RIB")
    insuranceDeadline = models.DateField(verbose_name="Date de fin d'assurance", blank=True, null=True)
    contractSigned = models.BooleanField(default=False, verbose_name="Contrat signé")
    contractDate = models.DateField(verbose_name="Date du contrat", blank=True, null=True)
    cautionRib = models.BooleanField(default=False, verbose_name="RIB caution")
    idgarant = models.BooleanField(default=False, verbose_name="Pièce d'identité du garant")
    payinslip = models.BooleanField(default=False, verbose_name="3 dernier bulletins de salaire du garant")
    tax_notice = models.BooleanField(default=False, verbose_name="Avis d'imposition du garant")
    stranger = models.BooleanField(default=False, verbose_name="Locataire étranger")
    caf = models.CharField(max_length=255, verbose_name="CAF", blank=True)
    residence_certificate = models.BooleanField(default=False, verbose_name="Certificat de domicile")
    check_guarantee = models.BooleanField(default=False, verbose_name="Chèque pour le complément de dépot de garantie")
    guarantee = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Garantie", blank=True, null=True)
    issue = models.BooleanField(default=False, verbose_name="Problème")
    missing_documents = models.TextField(verbose_name="Documents manquants", blank=True)
    date_of_entry = models.DateField(verbose_name="Date d'entrée", blank=True, null=True)
    date_of_departure = models.DateField(verbose_name="Date de sortie", blank=True, null=True)
    

    def __str__(self):
        if(self.date_of_entry):
            a = str(self.date_of_entry)
        else:
            a = "?"
        if(self.date_of_departure):
            b = str(self.date_of_departure)
        else:
            b = "?"
        return str(self.tenant) + " dans " + str(self.room) + " (" + a + " - " + b + ")"

class Map(models.Model):
    class Meta:
        verbose_name="Plan"
    name = models.CharField(max_length=255, verbose_name="Nom")
    map = models.ImageField(verbose_name="Plan")

    def __str__(self):
        return self.name
