from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UrgencyRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(db_index=True, max_length=24, unique=True)),
                (
                    "problem_type",
                    models.CharField(
                        choices=[
                            ("site_down", "Site inaccessible"),
                            ("suspected_hack", "Suspicion de piratage"),
                            ("broken_form", "Formulaire cassé"),
                            ("email_dns_domain", "Problème email / DNS / domaine"),
                            ("content_modified", "Contenu modifié"),
                            ("critical_error", "Erreur critique"),
                            ("massive_slowdown", "Ralentissement massif"),
                            ("other", "Autre"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "impact_level",
                    models.CharField(
                        choices=[
                            ("minor", "Simple gêne"),
                            ("disrupted", "Activité perturbée"),
                            ("blocked", "Activité bloquée"),
                            ("security_data_risk", "Risque sécurité / données"),
                        ],
                        max_length=32,
                    ),
                ),
                ("affected_url", models.URLField(max_length=240)),
                ("short_description", models.TextField(max_length=700)),
                ("since_when", models.CharField(max_length=120)),
                ("name", models.CharField(max_length=120)),
                ("organization", models.CharField(max_length=160)),
                ("email", models.EmailField(max_length=180)),
                ("phone", models.CharField(max_length=40)),
                (
                    "contact_preference",
                    models.CharField(
                        choices=[
                            ("email", "Email"),
                            ("phone", "Téléphone"),
                            ("either", "Email ou téléphone"),
                        ],
                        max_length=16,
                    ),
                ),
                ("callback_slot", models.CharField(max_length=160)),
                (
                    "expected_next_step",
                    models.CharField(
                        choices=[
                            ("understand_first", "Je veux d’abord comprendre ce qui se passe"),
                            ("quick_callback", "Je souhaite être rappelé rapidement"),
                            ("secure_before_action", "Je veux sécuriser la situation avant d’agir"),
                            ("prepare_intervention", "Je veux préparer une intervention si nécessaire"),
                            ("need_guidance", "Je ne sais pas encore, j’ai besoin d’être guidé"),
                        ],
                        max_length=32,
                    ),
                ),
                ("consent_to_contact", models.BooleanField(default=False)),
                ("no_secrets_confirmed", models.BooleanField(default=False)),
                ("status", models.CharField(default="open", max_length=24)),
                ("notification_status", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
