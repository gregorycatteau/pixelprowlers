from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .validators import validate_plain_text, validate_structured_entries


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            status=PublishableModel.Status.PUBLISHED,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
            archived_at__isnull=True,
        )


class PublishableModel(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        PUBLISHED = "published", "Publié"
        ARCHIVED = "archived", "Archivé"

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT, db_index=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    archived_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_%(app_label)s_%(class)s_items",
        editable=False,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_%(app_label)s_%(class)s_items",
        editable=False,
    )

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        errors = {}
        if self.status == self.Status.DRAFT:
            if self.published_at:
                errors["published_at"] = "Un brouillon ne peut pas avoir de date de publication."
            if self.archived_at:
                errors["archived_at"] = "Un brouillon ne peut pas avoir de date d'archivage."
        elif self.status == self.Status.PUBLISHED:
            if not self.published_at:
                errors["published_at"] = "Une publication exige une date de publication."
            if self.archived_at:
                errors["archived_at"] = "Un contenu publié ne peut pas avoir de date d'archivage."
        elif self.status == self.Status.ARCHIVED and not self.archived_at:
            errors["archived_at"] = "Une archive exige une date d'archivage."

        if self.published_at and self.archived_at and self.archived_at < self.published_at:
            errors["archived_at"] = "L'archivage ne peut pas précéder la publication."
        if errors:
            raise ValidationError(errors)


class RefurbishedMachine(PublishableModel):
    class CommercialStatus(models.TextChoices):
        AVAILABLE = "available", "Disponible"
        RESERVED = "reserved", "Réservée"
        SOLD = "sold", "Vendue"
        ARCHIVED = "archived", "Archivée"

    class Currency(models.TextChoices):
        EUR = "EUR", "EUR"

    internal_reference = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    title = models.CharField(max_length=180, blank=True, validators=[validate_plain_text])
    brand = models.CharField(max_length=100, blank=True, validators=[validate_plain_text])
    model_name = models.CharField(max_length=140, blank=True, validators=[validate_plain_text])
    summary = models.CharField(max_length=320, blank=True, validators=[validate_plain_text])
    description = models.TextField(blank=True, validators=[MaxLengthValidator(10_000), validate_plain_text])
    cosmetic_condition = models.CharField(max_length=240, blank=True, validators=[validate_plain_text])
    installed_operating_system = models.CharField(max_length=160, blank=True, validators=[validate_plain_text])
    specifications = models.JSONField(default=list, blank=True, validators=[validate_structured_entries])
    performed_interventions = models.JSONField(default=list, blank=True, validators=[validate_structured_entries])
    performed_tests = models.JSONField(default=list, blank=True, validators=[validate_structured_entries])
    commercial_status = models.CharField(
        max_length=16,
        choices=CommercialStatus.choices,
        default=CommercialStatus.AVAILABLE,
        db_index=True,
    )
    price_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.EUR)
    warranty_information = models.CharField(max_length=300, blank=True, validators=[validate_plain_text])
    availability_note = models.CharField(max_length=300, blank=True, validators=[validate_plain_text])
    featured = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=60, blank=True, validators=[validate_plain_text])
    seo_description = models.CharField(max_length=160, blank=True, validators=[validate_plain_text])
    available_since = models.DateField(blank=True, null=True)
    reserved_at = models.DateTimeField(blank=True, null=True)
    sold_at = models.DateTimeField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, validators=[MaxLengthValidator(5_000), validate_plain_text])

    class Meta:
        ordering = ["-featured", "display_order", "-published_at", "id"]
        permissions = [
            ("edit_refurbishedmachine_drafts", "Peut modifier les brouillons du catalogue"),
            ("publish_refurbishedmachine", "Peut publier les machines reconditionnées"),
            ("change_refurbishedmachine_commercial_status", "Peut changer le statut commercial"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price_amount__isnull=True) | models.Q(price_amount__gte=0),
                name="catalogue_machine_price_non_negative",
            ),
        ]

    def __str__(self):
        return f"{self.title or self.internal_reference} ({self.internal_reference})"

    def clean(self):
        super().clean()
        errors = {}
        original = None
        if self.pk:
            original = type(self).objects.filter(pk=self.pk).values(
                "internal_reference", "slug", "status"
            ).first()

        if original and original["internal_reference"] != self.internal_reference:
            if not getattr(self, "_allow_internal_reference_change", False):
                errors["internal_reference"] = "La référence interne est immuable après création."
        if original and original["status"] in {self.Status.PUBLISHED, self.Status.ARCHIVED}:
            if original["slug"] != self.slug:
                errors["slug"] = "Le slug est immuable après la première publication."

        required_for_publication = {
            "slug": self.slug,
            "title": self.title,
            "brand": self.brand,
            "model_name": self.model_name,
            "summary": self.summary,
            "cosmetic_condition": self.cosmetic_condition,
            "installed_operating_system": self.installed_operating_system,
            "specifications": self.specifications,
            "performed_tests": self.performed_tests,
        }
        if self.status == self.Status.PUBLISHED:
            for field, value in required_for_publication.items():
                if not value:
                    errors[field] = "Ce champ est obligatoire pour publier la machine."

        if self.commercial_status == self.CommercialStatus.AVAILABLE:
            if self.reserved_at:
                errors["reserved_at"] = "Une machine disponible ne peut pas avoir de date de réservation."
            if self.sold_at:
                errors["sold_at"] = "Une machine disponible ne peut pas avoir de date de vente."
        elif self.commercial_status == self.CommercialStatus.RESERVED:
            if not self.reserved_at:
                errors["reserved_at"] = "Une machine réservée exige une date de réservation."
            if self.sold_at:
                errors["sold_at"] = "Une machine réservée ne peut pas avoir de date de vente."
        elif self.commercial_status == self.CommercialStatus.SOLD and not self.sold_at:
            errors["sold_at"] = "Une machine vendue exige une date de vente."

        if self.sold_at and self.reserved_at and self.sold_at < self.reserved_at:
            errors["sold_at"] = "La vente ne peut pas précéder la réservation."
        if self.commercial_status == self.CommercialStatus.ARCHIVED and not self.archived_at:
            errors["archived_at"] = "Une machine commercialement archivée exige une date d'archivage."
        if self.status == self.Status.ARCHIVED and self.commercial_status != self.CommercialStatus.ARCHIVED:
            errors["commercial_status"] = "Une archive éditoriale doit aussi être archivée commercialement."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def publish(self, *, at=None):
        if self.status == self.Status.PUBLISHED:
            return False
        self.status = self.Status.PUBLISHED
        self.published_at = at or timezone.now()
        self.archived_at = None
        self.save()
        return True

    def archive(self, *, at=None):
        if self.status == self.Status.ARCHIVED and self.commercial_status == self.CommercialStatus.ARCHIVED:
            return False
        self.status = self.Status.ARCHIVED
        self.commercial_status = self.CommercialStatus.ARCHIVED
        self.archived_at = at or timezone.now()
        self.save()
        return True

    def mark_available(self):
        changed = self.commercial_status != self.CommercialStatus.AVAILABLE or self.reserved_at or self.sold_at
        self.commercial_status = self.CommercialStatus.AVAILABLE
        self.reserved_at = None
        self.sold_at = None
        self.save()
        return bool(changed)

    def mark_reserved(self, *, at=None):
        if self.commercial_status == self.CommercialStatus.RESERVED:
            return False
        self.commercial_status = self.CommercialStatus.RESERVED
        self.reserved_at = at or timezone.now()
        self.sold_at = None
        self.save()
        return True

    def mark_sold(self, *, at=None):
        if self.commercial_status == self.CommercialStatus.SOLD:
            return False
        self.commercial_status = self.CommercialStatus.SOLD
        self.sold_at = at or timezone.now()
        self.save()
        return True
