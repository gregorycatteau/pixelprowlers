from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AuditDossier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero_dossier", models.CharField(db_index=True, max_length=16, unique=True)),
                ("prenom", models.CharField(max_length=80)),
                ("nom", models.CharField(max_length=80)),
                ("email", models.EmailField(max_length=180)),
                ("telephone", models.CharField(max_length=24)),
                (
                    "type_personne",
                    models.CharField(
                        choices=[
                            ("individu", "Individu"),
                            ("association", "Association"),
                            ("entreprise", "Entreprise"),
                        ],
                        max_length=16,
                    ),
                ),
                ("nom_structure", models.CharField(blank=True, max_length=180, null=True)),
                ("consentement_rgpd", models.BooleanField(default=False)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("identifié", "Identifié"),
                            ("questionnaire_complété", "Questionnaire complété"),
                        ],
                        default="identifié",
                        max_length=32,
                    ),
                ),
                ("notification_status", models.JSONField(blank=True, default=dict)),
            ],
            options={"ordering": ["-date_creation"]},
        ),
        migrations.CreateModel(
            name="AuditDossierCounter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("year", models.PositiveIntegerField(unique=True)),
                ("last_number", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["-year"]},
        ),
        migrations.CreateModel(
            name="AuditReponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reponses", models.JSONField()),
                ("scores_series", models.JSONField()),
                ("score_global", models.DecimalField(decimal_places=2, max_digits=4)),
                ("pilier_faible", models.CharField(max_length=80)),
                ("date_soumission", models.DateTimeField(auto_now_add=True)),
                (
                    "dossier",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reponse",
                        to="audits.auditdossier",
                    ),
                ),
            ],
            options={"ordering": ["-date_soumission"]},
        ),
    ]
