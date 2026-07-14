import hashlib
import hmac
import json
import unicodedata
from collections import defaultdict
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


PARIS = ZoneInfo("Europe/Paris")
UTC = ZoneInfo("UTC")


def _text(value):
    return unicodedata.normalize("NFC", value or "")


def backfill_contact_dossiers(apps, schema_editor):
    secret = getattr(settings, "CONTACT_HMAC_SECRET", "")
    if not secret:
        raise RuntimeError("CONTACT_HMAC_SECRET is required to migrate existing contact dossiers.")

    Contact = apps.get_model("crm", "Contact")
    Counter = apps.get_model("crm", "ContactDailyCounter")
    sequences = defaultdict(int)
    for contact in Contact.objects.order_by("created_at", "pk").iterator():
        created = contact.created_at or timezone.now()
        business_date = timezone.localtime(created, PARIS).date()
        sequences[business_date] += 1
        if sequences[business_date] > 999:
            raise RuntimeError(f"More than 999 contacts exist for business date {business_date}.")
        if sequences[business_date] > 999:
            raise RuntimeError(f"More than 999 historical contacts exist for {business_date.isoformat()}.")

        parts = (contact.name or "").strip().split(maxsplit=1)
        contact.prenom = (parts[0] if parts else "Non renseigné")[:100]
        contact.nom = (parts[1] if len(parts) > 1 else "Non renseigné")[:100]
        contact.objet = contact.demand_type or contact.service_type or "Demande de contact"
        contact.methode_contact = "email"
        contact.date_creation = created
        contact.numero_dossier = f"{business_date:%d%m%Y}{sequences[business_date]:03d}"
        canonical = {
            "date_creation": created.astimezone(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z"),
            "email": _text(contact.email),
            "message": _text(contact.message),
            "methode_contact": contact.methode_contact,
            "nom": _text(contact.nom),
            "numero_dossier": contact.numero_dossier,
            "objet": _text(contact.objet),
            "prenom": _text(contact.prenom),
            "telephone": _text(contact.phone),
        }
        encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        contact.signature_hmac = hmac.new(secret.encode("utf-8"), encoded, hashlib.sha256).hexdigest()
        contact.save(
            update_fields=[
                "numero_dossier",
                "nom",
                "prenom",
                "objet",
                "methode_contact",
                "date_creation",
                "signature_hmac",
            ]
        )

    Counter.objects.bulk_create(
        [Counter(date=date, value=value) for date, value in sequences.items()],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):
    dependencies = [("crm", "0002_contact_demand_type_contact_secret_token_and_more")]

    operations = [
        migrations.CreateModel(
            name="ContactDailyCounter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(unique=True)),
                ("value", models.PositiveSmallIntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-date"],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("value__lte", 999)),
                        name="crm_contact_daily_counter_max_999",
                    )
                ],
            },
        ),
        migrations.AddField("contact", "date_creation", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("contact", "date_notification", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("contact", "methode_contact", models.CharField(blank=True, max_length=16, null=True)),
        migrations.AddField("contact", "nom", models.CharField(blank=True, max_length=100, null=True)),
        migrations.AddField("contact", "numero_dossier", models.CharField(blank=True, max_length=11, null=True, unique=True)),
        migrations.AddField("contact", "objet", models.CharField(blank=True, max_length=200, null=True)),
        migrations.AddField("contact", "prenom", models.CharField(blank=True, max_length=100, null=True)),
        migrations.AddField("contact", "signature_hmac", models.CharField(blank=True, max_length=64, null=True)),
        migrations.AddField(
            "contact",
            "statut_notification",
            models.CharField(db_index=True, default="en_attente", max_length=16),
        ),
        migrations.AlterField("contact", "email", models.EmailField(db_index=True, max_length=254)),
        migrations.RunPython(backfill_contact_dossiers, migrations.RunPython.noop),
        migrations.AlterField("contact", "date_creation", models.DateTimeField(db_index=True, default=timezone.now)),
        migrations.AlterField(
            "contact",
            "methode_contact",
            models.CharField(
                choices=[("email", "Email"), ("telephone", "Téléphone"), ("les_deux", "Email et téléphone")],
                max_length=16,
            ),
        ),
        migrations.AlterField("contact", "nom", models.CharField(max_length=100)),
        migrations.AlterField("contact", "numero_dossier", models.CharField(max_length=11, unique=True)),
        migrations.AlterField("contact", "objet", models.CharField(max_length=200)),
        migrations.AlterField("contact", "prenom", models.CharField(max_length=100)),
        migrations.AlterField("contact", "signature_hmac", models.CharField(max_length=64)),
        migrations.AlterField(
            "contact",
            "statut_notification",
            models.CharField(
                choices=[("en_attente", "En attente"), ("envoyee", "Envoyée"), ("echec", "Échec")],
                db_index=True,
                default="en_attente",
                max_length=16,
            ),
        ),
        migrations.AddConstraint(
            "contact",
            models.CheckConstraint(
                condition=models.Q(("numero_dossier__regex", "^[0-9]{11}$")),
                name="crm_contact_numero_dossier_format",
            ),
        ),
        migrations.AddConstraint(
            "contact",
            models.CheckConstraint(
                condition=models.Q(("signature_hmac__regex", "^[0-9a-f]{64}$")),
                name="crm_contact_signature_hmac_format",
            ),
        ),
        migrations.AddConstraint(
            "contact",
            models.CheckConstraint(
                condition=models.Q(("methode_contact", "email"), ("phone__regex", ".*\\S.*"), _connector="OR"),
                name="crm_contact_phone_required",
            ),
        ),
    ]
