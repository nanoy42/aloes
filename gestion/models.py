"""Models of gestion app."""
from colorfield.fields import ColorField
from django.db import models


class School(models.Model):
    """Store a school."""
    class Meta:
        verbose_name = "Ecole"
    name = models.CharField(max_length=255, verbose_name="Nom de l'école")

    def __str__(self):
        return self.name

class Renovation(models.Model):
    """Store a renovation level."""
    name = models.CharField(max_length=255, verbose_name="Nom du niveau")
    description = models.TextField()
    color = ColorField(default="#FF0000", verbose_name="Couleur :")

    def __str__(self):
        return self.name

class Rent(models.Model):
    """Store a rent type."""
    class Meta:
        verbose_name = "Loyer"

    type = models.TextField(max_length=255, verbose_name="Genre")
    rent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Loyer")
    service = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Forfait services")
    charges = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Charges")
    application_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Frais de dossier"
    )
    surface = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Superficie")

    def __str__(self):
        return self.type + " (" + str(self.surface) + " m2)"

    @property
    def supplements(self):
        """Return supplements of rent which is service + charges."""
        return self.service + self.charges

    @property
    def total_rent(self):
        """Return the total rent which is the rent + supplements."""
        return self.rent + self.supplements

class Tenant(models.Model):
    """Store a tenant."""
    class Meta:
        verbose_name = "Locataire"

    GENDER_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    name = models.CharField(max_length=255, verbose_name="Nom")
    first_name = models.CharField(max_length=255, verbose_name="Prénom")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Sexe")
    school = models.ForeignKey('School', on_delete=models.PROTECT, verbose_name="Ecole", null=True)
    school_year = models.PositiveIntegerField(
        default=1,
        verbose_name="Année d'étude",
        blank=True,
        null=True
    )
    date_of_entry = models.DateField(verbose_name="Date d'entrée à la résidence", blank=True, null=True)
    date_of_departure = models.DateField(
        blank=True,
        verbose_name="Date de sortie de la résidence",
        null=True
    )
    observations = models.TextField(verbose_name="Observations", blank=True)
    temporary = models.BooleanField(default=False, verbose_name="Passager")
    cellphone = models.CharField(
        max_length=10,
        verbose_name="Numéro de téléphone portable",
        blank=True
    )
    leaving = models.BooleanField(default=False, verbose_name="Sur le départ")
    waterproof_undersheet = models.BooleanField(default=False, verbose_name="Alèse")
    pillow = models.BooleanField(default=False, verbose_name="Oreiller")
    pillowcase = models.BooleanField(default=False, verbose_name="Taie d'oreiller")
    blanket = models.BooleanField(default=False, verbose_name="Couverture")
    sheet = models.BooleanField(default=False, verbose_name="Drap")
    birthday = models.DateField(verbose_name="Date de naissance", blank=True, null=True)
    birthcity = models.CharField(max_length=255, verbose_name="Ville de naissance", blank=True)
    birthdepartement = models.CharField(
        max_length=255,
        verbose_name="Département de naissance",
        blank=True
    )
    birthcountry = models.CharField(max_length=255, verbose_name="Pays de naissance", blank=True)
    street_number = models.CharField(max_length=255, verbose_name="N° de rue", blank=True, null=True)
    street = models.CharField(max_length=255, verbose_name="Rue", blank=True)
    zipcode = models.PositiveIntegerField(verbose_name="Code postal", blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name="Ville", blank=True)
    country = models.CharField(max_length=255, verbose_name="Pays", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=10, verbose_name="Téléphone fixe", blank=True)
    current_leasing = models.ForeignKey(
        'Leasing',
        on_delete=models.PROTECT,
        verbose_name="Dossier actuel",
        blank=True,
        null=True,
        related_name="current_tenants"
    )
    next_leasing = models.ForeignKey(
        'Leasing',
        on_delete=models.PROTECT,
        verbose_name="Dossier suivant",
        blank=True,
        null=True,
        related_name="next_tenant"
    )

    def __str__(self):
        if self.gender == "M":
            pre = "M."
        else:
            pre = "Mme."
        return pre + " " + self.first_name + " " + self.name

    @property
    def room(self):
        """Return current room (if exists)."""
        if self.current_leasing:
            return self.current_leasing.room
        return None

    @property
    def next_room(self):
        """Return next room (if exists)."""
        if self.next_leasing:
            return self.next_leasing.room
        return None

    @property
    def previous_leasings(self):
        """Return all leasings of the tenant, except for current and next (if they exist)."""
        leasings = Leasing.objects.filter(tenant=self)
        if self.current_leasing:
            leasings = leasings.exclude(pk=self.current_leasing.pk)
        if self.next_leasing:
            leasings = leasings.exclude(pk=self.next_leasing.pk)
        return leasings.order_by('-date_of_entry')

    @property
    def previous_rooms(self):
        """Return all roomss of the tenant, excpet for current and next (if they exist)."""
        pks = [leasing.room.pk for leasing in self.previous_leasings]
        return Room.objects.filter(pk__in=pks)

    @property
    def civil_status_completed(self):
        """Return true if name, first_name, gender and school are completed."""
        return bool(self.name) and bool(self.first_name) and bool(self.gender) and bool(self.school)

    @property
    def birth_completed(self):
        """Return true if all birth information is completed."""
        return bool(self.birthday) and bool(self.birthcity) and bool(self.birthdepartement) and bool(self.birthcountry)

    @property
    def address_completed(self):
        """Return true if all current address information is completed."""
        return bool(self.street_number) and bool(self.street) and bool(self.city) and bool(self.country)

    @property
    def phone_mail_completed(self):
        """Return true if email, phone and cellphone are completed."""
        return bool(self.email) and bool(self.cellphone) and bool(self.phone)

    @property
    def completed(self):
        """Return true if civil_status, birth information,
        address information and contact information are completed."""
        return (bool(self.civil_status_completed) and bool(self.birth_completed)
                and bool(self.address_completed) and bool(self.phone_mail_completed))

class Room(models.Model):
    """Store a room."""
    EMPTY_CC = "table-warning"
    TEMPORARY_CC = "table-primary"
    LEAVING_CC = "table-success"
    NONE_CC = ""

    class Meta:
        verbose_name = "Chambre"

    lot = models.PositiveIntegerField(verbose_name="Lot", unique=True)
    room = models.CharField(max_length=6, verbose_name="Chambre", unique=True)
    rent_type = models.ForeignKey('Rent', on_delete=models.PROTECT, verbose_name="Loyer")
    renovation = models.ForeignKey(
        'Renovation',
        on_delete=models.PROTECT,
        verbose_name="Niveau de rénovation",
        blank=True,
        null=True
    )
    observations = models.TextField(verbose_name="Observations", blank=True)
    map = models.ImageField(verbose_name="Plan", blank=True, null=True)
    current_leasing = models.ForeignKey(
        'Leasing',
        on_delete=models.PROTECT,
        verbose_name="Dossier actuel",
        blank=True,
        null=True,
        related_name="current_rooms"
    )
    next_leasing = models.ForeignKey(
        'Leasing',
        on_delete=models.PROTECT,
        verbose_name="Dossier suivant",
        blank=True,
        null=True,
        related_name="next_rooms"
    )
    is_active = models.BooleanField(default=True, verbose_name="Chambre active ?")

    def __str__(self):
        return self.room

    def building(self):
        """Return building of the room i.e. the first char of room."""
        return self.room[0]

    @property
    def current_tenant(self):
        """Return current tenant (if exists)."""
        if self.current_leasing:
            return self.current_leasing.tenant
        return None

    @property
    def next_tenant(self):
        """Return next tenant (if exists)."""
        if self.next_leasing:
            return self.next_leasing.tenant
        else:
            return Leasing

    @property
    def previous_leasings(self):
        """Return all leasings of the room, except for current and next (if they exist)."""
        leasings = Leasing.objects.filter(room=self)
        if self.current_leasing:
            leasings = leasings.exclude(pk=self.current_leasing.pk)
        if self.next_leasing:
            leasings = leasings.exclude(pk=self.next_leasing.pk)
        return leasings.order_by('-date_of_entry')

    @property
    def previous_tenants(self):
        """Return all tenants of the room, except for current and next (if they exist)."""
        pks = [leasing.tenant.pk for leasing in self.previous_leasings]
        return Tenant.objects.filter(pk__in=pks)

    @property
    def color_class(self):
        """Return the appropriate color class."""
        if self.current_leasing:
            if self.current_leasing.tenant.leaving:
                return self.LEAVING_CC
            elif self.current_leasing.tenant.temporary:
                return self.TEMPORARY_CC
            else:
                return self.NONE_CC
        else:
            return self.EMPTY_CC


class Leasing(models.Model):
    """Store a leasing."""
    class Meta:
        verbose_name = "Location"

    PAYMENT_CHOICES = (
        ('direct_debit', 'Prélèvement'),
        ('bank_transfer', 'Virement'),
        ('check', 'Chèque'),
        ('cash', 'Espèces'),
        ('special', 'Special'),
    )
    tenant = models.ForeignKey('Tenant', on_delete=models.PROTECT, verbose_name="Locataire")
    room = models.ForeignKey('Room', on_delete=models.PROTECT, verbose_name="Chambre")
    bail = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Caution",
        blank=True,
        null=True
    )
    apl = models.DateField(verbose_name="APL", blank=True, null=True)
    payment = models.CharField(
        max_length=255,
        verbose_name="Paiement",
        choices=PAYMENT_CHOICES,
        blank=True
    )
    rib = models.BooleanField(default=False, verbose_name="RIB")
    insuranceDeadline = models.DateField(
        verbose_name="Date de fin d'assurance",
        blank=True,
        null=True
    )
    contract_signed = models.BooleanField(default=False, verbose_name="Contrat signé")
    contract_date = models.DateField(verbose_name="Date du contrat", blank=True, null=True)
    caution_rib = models.BooleanField(default=False, verbose_name="RIB caution")
    idgarant = models.BooleanField(default=False, verbose_name="Pièce d'identité du garant")
    payinslip = models.BooleanField(
        default=False,
        verbose_name="3 dernier bulletins de salaire du garant"
    )
    tax_notice = models.BooleanField(default=False, verbose_name="Avis d'imposition du garant")
    stranger = models.BooleanField(default=False, verbose_name="Locataire étranger")
    caf = models.CharField(max_length=255, verbose_name="CAF", blank=True)
    residence_certificate = models.BooleanField(
        default=False,
        verbose_name="Certificat de domicile"
    )
    check_guarantee = models.BooleanField(
        default=False,
        verbose_name="Chèque pour le complément de dépot de garantie"
    )
    guarantee = models.BooleanField(default=False, verbose_name="Engagement de caution")
    photo = models.BooleanField(default=False, verbose_name="Photo d'identité")
    internal_rules_signed = models.BooleanField(
        default=False,
        verbose_name="Règlement intérieur signé"
    )
    school_certificate = models.BooleanField(default=False, verbose_name="Certificat de scolarité")
    debit_authorization = models.BooleanField(
        default=False,
        verbose_name="Autorisation de prélèvement"
    )
    issue = models.BooleanField(default=False, verbose_name="Problème")
    missing_documents = models.TextField(verbose_name="Documents manquants", blank=True)
    date_of_entry = models.DateField(verbose_name="Date d'entrée", blank=True, null=True)
    date_of_departure = models.DateField(verbose_name="Date de sortie", blank=True, null=True)

    def __str__(self):
        date1 = date2 = "?"
        if self.date_of_entry:
            date1 = self.date_of_entry.strftime('%d/%m/%Y')
        if self.date_of_departure:
            date2 = self.date_of_departure.strftime('%d/%m/%Y')
        return str(self.tenant) + \
        " dans " + str(self.room) + \
        " (" + date1 + \
        " - " + date2 + ")"

class Map(models.Model):
    """Store a general map."""
    class Meta:
        verbose_name = "Plan"
    name = models.CharField(max_length=255, verbose_name="Nom")
    map = models.ImageField(verbose_name="Plan")

    def __str__(self):
        return self.name
