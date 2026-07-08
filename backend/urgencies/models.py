from django.db import models


class UrgencyRequest(models.Model):
    class ProblemType(models.TextChoices):
        SITE_DOWN = "site_down", "Site inaccessible"
        SUSPECTED_HACK = "suspected_hack", "Suspicion de piratage"
        BROKEN_FORM = "broken_form", "Formulaire cassé"
        EMAIL_DNS_DOMAIN = "email_dns_domain", "Problème email / DNS / domaine"
        CONTENT_MODIFIED = "content_modified", "Contenu modifié"
        CRITICAL_ERROR = "critical_error", "Erreur critique"
        MASSIVE_SLOWDOWN = "massive_slowdown", "Ralentissement massif"
        OTHER = "other", "Autre"

    class ImpactLevel(models.TextChoices):
        MINOR = "minor", "Simple gêne"
        DISRUPTED = "disrupted", "Activité perturbée"
        BLOCKED = "blocked", "Activité bloquée"
        SECURITY_DATA_RISK = "security_data_risk", "Risque sécurité / données"

    class ContactPreference(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Téléphone"
        EITHER = "either", "Email ou téléphone"

    class ExpectedNextStep(models.TextChoices):
        UNDERSTAND_FIRST = "understand_first", "Je veux d’abord comprendre ce qui se passe"
        QUICK_CALLBACK = "quick_callback", "Je souhaite être rappelé rapidement"
        SECURE_BEFORE_ACTION = "secure_before_action", "Je veux sécuriser la situation avant d’agir"
        PREPARE_INTERVENTION = "prepare_intervention", "Je veux préparer une intervention si nécessaire"
        NEED_GUIDANCE = "need_guidance", "Je ne sais pas encore, j’ai besoin d’être guidé"

    reference = models.CharField(max_length=24, unique=True, db_index=True)
    problem_type = models.CharField(max_length=32, choices=ProblemType.choices)
    impact_level = models.CharField(max_length=32, choices=ImpactLevel.choices)
    affected_url = models.URLField(max_length=240)
    short_description = models.TextField(max_length=700)
    since_when = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    organization = models.CharField(max_length=160)
    email = models.EmailField(max_length=180)
    phone = models.CharField(max_length=40)
    contact_preference = models.CharField(max_length=16, choices=ContactPreference.choices)
    callback_slot = models.CharField(max_length=160)
    expected_next_step = models.CharField(max_length=32, choices=ExpectedNextStep.choices)
    consent_to_contact = models.BooleanField(default=False)
    no_secrets_confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=24, default="open")
    notification_status = models.JSONField(default=dict, blank=True)
    client_dossier = models.ForeignKey(
        "audits.ClientDossier",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="urgency_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.reference
