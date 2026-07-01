from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(TimeStampedModel):
    SERVICE_AUDIT_SITE = 'audit_site'
    SERVICE_SITE_MAINTENABLE = 'site_maintenable'
    SERVICE_MAINTENANCE_DOCUMENTATION = 'maintenance_documentation'
    SERVICE_URGENCE = 'urgence'
    SERVICE_DEVELOPPEMENT = 'developpement'
    SERVICE_MATERIEL = 'materiel'
    SERVICE_FORMATION = 'formation'
    SERVICE_AUTRE = 'autre'

    SERVICE_CHOICES = [
        (SERVICE_AUDIT_SITE, 'Audit sécurité de site web'),
        (SERVICE_SITE_MAINTENABLE, 'Site sobre, sécurisé, maintenable'),
        (SERVICE_MAINTENANCE_DOCUMENTATION, 'Maintenance, accès et documentation'),
        (SERVICE_URGENCE, 'Urgence : site cassé, piraté ou inaccessible'),
        (SERVICE_DEVELOPPEMENT, 'Développement Web/Applicatif'),
        (SERVICE_MATERIEL, 'Réparation/Reconditionnement'),
        (SERVICE_FORMATION, 'Formation & Hygiène Numérique'),
        (SERVICE_AUTRE, 'Autre'),
    ]

    name = models.CharField(max_length=160)
    email = models.EmailField()
    company = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    service_type = models.CharField(max_length=32, choices=SERVICE_CHOICES)
    message = models.TextField()
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} - {self.email}'


class Lead(TimeStampedModel):
    LEAD_DEV = 'developpement'
    LEAD_MATERIEL = 'materiel'
    LEAD_FORMATION = 'formation'
    LEAD_AUTRE = 'autre'

    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_QUALIFIED = 'qualified'
    STATUS_CLOSED = 'closed'

    LEAD_TYPE_CHOICES = [
        (LEAD_DEV, 'Développement'),
        (LEAD_MATERIEL, 'Matériel'),
        (LEAD_FORMATION, 'Formation'),
        (LEAD_AUTRE, 'Autre'),
    ]
    STATUS_CHOICES = [
        (STATUS_NEW, 'Nouveau'),
        (STATUS_CONTACTED, 'Contacté'),
        (STATUS_QUALIFIED, 'Qualifié'),
        (STATUS_CLOSED, 'Clôturé'),
    ]

    name = models.CharField(max_length=160)
    email = models.EmailField()
    company = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    budget = models.CharField(max_length=80, blank=True)
    project_description = models.TextField()
    timeline = models.CharField(max_length=120, blank=True)
    lead_type = models.CharField(max_length=32, choices=LEAD_TYPE_CHOICES)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_NEW)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} - {self.lead_type}'


class Formation(TimeStampedModel):
    FORMAT_PRESENTIEL = 'presentiel'
    FORMAT_DISTANCIEL = 'distanciel'
    FORMAT_HYBRIDE = 'hybride'

    FORMAT_CHOICES = [
        (FORMAT_PRESENTIEL, 'Présentiel'),
        (FORMAT_DISTANCIEL, 'Distanciel'),
        (FORMAT_HYBRIDE, 'Hybride'),
    ]

    title = models.CharField(max_length=180)
    description = models.TextField()
    format_type = models.CharField(max_length=32, choices=FORMAT_CHOICES)
    duration_hours = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_participants = models.PositiveIntegerField(default=10)
    scheduled_dates = models.JSONField(default=list, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class FormationRegistration(TimeStampedModel):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'En attente'),
        (STATUS_CONFIRMED, 'Confirmée'),
        (STATUS_CANCELLED, 'Annulée'),
    ]

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=160)
    email = models.EmailField()
    company = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    number_of_participants = models.PositiveIntegerField(default=1)
    special_needs = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} - {self.formation}'


class Service(TimeStampedModel):
    CATEGORY_DEV = 'developpement'
    CATEGORY_MATERIEL = 'materiel'
    CATEGORY_FORMATION = 'formation'

    CATEGORY_CHOICES = [
        (CATEGORY_DEV, 'Développement'),
        (CATEGORY_MATERIEL, 'Matériel'),
        (CATEGORY_FORMATION, 'Formation'),
    ]

    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=80, blank=True)
    service_category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self) -> str:
        return self.name
