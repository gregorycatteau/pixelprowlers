from django.db import migrations, models


SEED_CITATIONS = [
    {
        "texte": "Il vient toujours une heure où protester ne suffit plus : après la philosophie, il faut l'action.",
        "auteur": "Victor Hugo",
        "source": "Les Misérables",
    },
    {
        "texte": "Le plus grand arbre est né d'une graine menue.",
        "auteur": "Lao Tseu",
        "source": "Tao Te King",
    },
    {
        "texte": "Il y a un temps pour tout, et un temps pour toute chose sous les cieux.",
        "auteur": "Ecclésiaste",
        "source": "Ecclésiaste 3:1",
    },
    {
        "texte": "Même la nuit la plus sombre prendra fin et le soleil se lèvera.",
        "auteur": "Victor Hugo",
        "source": "Les Misérables",
    },
    {
        "texte": "Il n'est jamais trop tard pour devenir ce que nous aurions pu être.",
        "auteur": "George Eliot",
        "source": "",
    },
]


def seed_citations(apps, _schema_editor):
    citation = apps.get_model("audits", "Citation")

    for item in SEED_CITATIONS:
        citation.objects.get_or_create(
            texte=item["texte"],
            auteur=item["auteur"],
            defaults={
                "source": item["source"],
                "actif": True,
            },
        )


def remove_seed_citations(apps, _schema_editor):
    citation = apps.get_model("audits", "Citation")
    citation.objects.filter(texte__in=[item["texte"] for item in SEED_CITATIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("audits", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Citation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("texte", models.TextField()),
                ("auteur", models.CharField(max_length=140)),
                ("source", models.CharField(blank=True, max_length=180)),
                ("actif", models.BooleanField(default=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["auteur", "source", "id"]},
        ),
        migrations.RunPython(seed_citations, remove_seed_citations),
    ]
