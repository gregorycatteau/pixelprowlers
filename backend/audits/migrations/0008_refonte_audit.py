from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audits", "0007_rdv_models"),
    ]

    operations = [
        migrations.CreateModel(
            name="RefonteAudit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(db_index=True, max_length=28, unique=True)),
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
                ("site_url", models.URLField(max_length=500)),
                ("consentement_rgpd", models.BooleanField(default=False)),
                ("reponses", models.JSONField()),
                (
                    "analysis_status",
                    models.CharField(
                        choices=[
                            ("en_cours", "En cours d'analyse"),
                            ("termine", "Terminé"),
                            ("echec_partiel", "Échec partiel"),
                            ("non_analysable", "Non analysable"),
                            ("echec", "Échec"),
                        ],
                        default="en_cours",
                        max_length=24,
                    ),
                ),
                ("technical_report", models.JSONField(blank=True, default=dict)),
                ("pagespeed_report", models.JSONField(blank=True, default=dict)),
                ("heuristic_report", models.JSONField(blank=True, default=list)),
                ("analysis_error", models.TextField(blank=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("date_maj", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-date_creation"],
            },
        ),
        migrations.AddIndex(
            model_name="refonteaudit",
            index=models.Index(fields=["email"], name="refonte_email_idx"),
        ),
        migrations.AddIndex(
            model_name="refonteaudit",
            index=models.Index(fields=["analysis_status"], name="refonte_status_idx"),
        ),
    ]
