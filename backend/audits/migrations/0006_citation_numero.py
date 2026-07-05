from django.db import migrations, models


def populate_citation_numbers(apps, _schema_editor):
    citation = apps.get_model("audits", "Citation")

    for numero, item in enumerate(citation.objects.order_by("id"), start=1):
        item.numero = numero
        item.save(update_fields=["numero"])


def clear_citation_numbers(apps, _schema_editor):
    citation = apps.get_model("audits", "Citation")
    citation.objects.update(numero=None)


class Migration(migrations.Migration):
    dependencies = [
        ("audits", "0005_citation_extended_metadata"),
    ]

    operations = [
        migrations.AddField(
            model_name="citation",
            name="numero",
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True, unique=True),
        ),
        migrations.RunPython(populate_citation_numbers, clear_citation_numbers),
        migrations.AlterField(
            model_name="citation",
            name="numero",
            field=models.PositiveIntegerField(db_index=True, unique=True),
        ),
        migrations.AlterModelOptions(
            name="citation",
            options={"ordering": ["numero", "auteur", "source", "id"]},
        ),
    ]
