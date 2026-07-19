import secrets

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(TimeStampedModel):
    class ServiceType(models.TextChoices):
        AUDIT_SITE = "audit_site", "Audit sécurité de site web"
        SITE_MAINTENABLE = "site_maintenable", "Site sobre, sécurisé, maintenable"
        MAINTENANCE_DOCUMENTATION = "maintenance_documentation", "Maintenance, accès et documentation"
        URGENCE = "urgence", "Urgence : site cassé, piraté ou inaccessible"
        DEVELOPPEMENT = "developpement", "Développement Web/Applicatif"
        MATERIEL = "materiel", "Réparation/Reconditionnement"
        FORMATION = "formation", "Formation & Hygiène Numérique"
        AUTRE = "autre", "Autre"

    class Status(models.TextChoices):
        OPEN = "open", "Ouvert"
        IN_PROGRESS = "in_progress", "En cours"
        WAITING_CUSTOMER = "waiting_customer", "En attente client"
        RESOLVED = "resolved", "Résolu"
        CLOSED = "closed", "Clôturé"

    class DemandType(models.TextChoices):
        DIAGNOSTIC = "diagnostic", "Diagnostic"
        URGENCY = "urgency", "Urgence"
        AUDIT = "audit", "Audit"
        REFONTE = "refonte", "Refonte"
        TRANSMISSION = "transmission", "Transmission"
        MATERIEL = "materiel", "Matériel : réparation, reconditionnement, migration Linux"
        PARTNERSHIP = "partnership", "Partenariat / autre"

    class ContactMethod(models.TextChoices):
        EMAIL = "email", "Email"
        TELEPHONE = "telephone", "Téléphone"
        BOTH = "les_deux", "Email et téléphone"

    class NotificationStatus(models.TextChoices):
        PENDING = "en_attente", "En attente"
        SENT = "envoyee", "Envoyée"
        FAILED = "echec", "Échec"

    ticket_id = models.CharField(max_length=32, unique=True, blank=True)
    secret_token = models.CharField(max_length=64, unique=True, blank=True)
    numero_dossier = models.CharField(max_length=11, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    name = models.CharField(max_length=160)
    email = models.EmailField(db_index=True)
    company = models.CharField(max_length=180)
    phone = models.CharField(
        max_length=40,
        validators=[
            RegexValidator(
                regex=r"^0[67][0-9]{8}$",
                message="Le numéro de téléphone doit être un numéro français valide.",
            )
        ],
    )
    service_type = models.CharField(max_length=32, choices=ServiceType.choices)
    demand_type = models.CharField(max_length=32, choices=DemandType.choices)
    objet = models.CharField(max_length=200)
    methode_contact = models.CharField(max_length=16, choices=ContactMethod.choices)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.OPEN)
    message = models.TextField()
    read = models.BooleanField(default=False)
    statut_notification = models.CharField(
        max_length=16,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
        db_index=True,
    )
    date_notification = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now, db_index=True)
    signature_hmac = models.CharField(max_length=64)
    notification_status = models.JSONField(default=dict, blank=True)
    client_dossier = models.ForeignKey(
        "audits.ClientDossier",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="crm_contacts",
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(numero_dossier__regex=r"^[0-9]{11}$"),
                name="crm_contact_numero_dossier_format",
            ),
            models.CheckConstraint(
                condition=models.Q(signature_hmac__regex=r"^[0-9a-f]{64}$"),
                name="crm_contact_signature_hmac_format",
            ),
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.full_clean()
        if not self.ticket_id:
            self.ticket_id = f"CT-{secrets.token_urlsafe(6).replace('-', '').replace('_', '').upper()[:8]}"
        if not self.secret_token:
            self.secret_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.numero_dossier


class ContactDailyCounter(models.Model):
    date = models.DateField(unique=True)
    value = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(value__lte=999),
                name="crm_contact_daily_counter_max_999",
            ),
        ]

    def __str__(self) -> str:
        return self.date.isoformat()


class ContactMessage(TimeStampedModel):
    class Author(models.TextChoices):
        CUSTOMER = "customer", "Client"
        SUPPORT = "support", "Support"
        SYSTEM = "system", "Système"

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="messages")
    author = models.CharField(max_length=24, choices=Author.choices, default=Author.CUSTOMER)
    author_name = models.CharField(max_length=160)
    message = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.contact.ticket_id} - {self.author}"


class DiagnosticTicket(TimeStampedModel):
    ticket_id = models.CharField(max_length=32, unique=True, blank=True)
    organization = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=32, default="open")
    answers = models.JSONField(default=dict, blank=True)
    diagnostic_result = models.JSONField(default=dict, blank=True)
    email_confirmation = models.JSONField(default=dict, blank=True)
    client_dossier = models.ForeignKey(
        "audits.ClientDossier",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="diagnostic_tickets",
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = f"PP-{secrets.token_urlsafe(20)[:27]}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.ticket_id} - {self.email}"


class Lead(TimeStampedModel):
    class LeadType(models.TextChoices):
        DEVELOPPEMENT = "developpement", "Développement"
        MATERIEL = "materiel", "Matériel"
        FORMATION = "formation", "Formation"
        AUTRE = "autre", "Autre"

    class Status(models.TextChoices):
        NEW = "new", "Nouveau"
        CONTACTED = "contacted", "Contacté"
        QUALIFIED = "qualified", "Qualifié"
        CLOSED = "closed", "Clôturé"

    name = models.CharField(max_length=160)
    email = models.EmailField()
    company = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    budget = models.CharField(max_length=80, blank=True)
    project_description = models.TextField()
    timeline = models.CharField(max_length=120, blank=True)
    lead_type = models.CharField(max_length=32, choices=LeadType.choices)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.NEW)
    client_dossier = models.ForeignKey(
        "audits.ClientDossier",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="crm_leads",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.lead_type}"


class Formation(TimeStampedModel):
    class FormatType(models.TextChoices):
        PRESENTIEL = "presentiel", "Présentiel"
        DISTANCIEL = "distanciel", "Distanciel"
        HYBRIDE = "hybride", "Hybride"

    title = models.CharField(max_length=180)
    description = models.TextField()
    format_type = models.CharField(max_length=32, choices=FormatType.choices)
    duration_hours = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_participants = models.PositiveIntegerField(default=10)
    scheduled_dates = models.JSONField(default=list, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class FormationRegistration(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        CONFIRMED = "confirmed", "Confirmée"
        CANCELLED = "cancelled", "Annulée"

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="registrations")
    name = models.CharField(max_length=160)
    email = models.EmailField()
    company = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    number_of_participants = models.PositiveIntegerField(default=1)
    special_needs = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.PENDING)
    client_dossier = models.ForeignKey(
        "audits.ClientDossier",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="formation_registrations",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.formation}"


class Service(TimeStampedModel):
    class Category(models.TextChoices):
        DEVELOPPEMENT = "developpement", "Développement"
        MATERIEL = "materiel", "Matériel"
        FORMATION = "formation", "Formation"

    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=80, blank=True)
    service_category = models.CharField(max_length=32, choices=Category.choices)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name
