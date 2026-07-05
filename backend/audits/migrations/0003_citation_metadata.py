import json
import re
import unicodedata
from pathlib import Path

from django.db import migrations, models


MULTIPLE_SPACES_PATTERN = re.compile(r"\s+")
FINAL_PUNCTUATION_PATTERN = re.compile(r"[\s\.,;:!?…\"'»”’\)\]]+$")


def normalize_text(value):
    normalized = unicodedata.normalize("NFC", value or "")
    normalized = MULTIPLE_SPACES_PATTERN.sub(" ", normalized)
    return normalized.strip()


def normalize_dedupe_key(value):
    return FINAL_PUNCTUATION_PATTERN.sub("", normalize_text(value)).casefold()


def backfill_imported_citation_metadata(apps, _schema_editor):
    citation = apps.get_model("audits", "Citation")
    backend_dir = Path(__file__).resolve().parents[2]
    imports_dir = backend_dir / "audits" / "fixtures" / "imports"
    lot_paths = [
        imports_dir / "lot_citations_01.json",
        imports_dir / "lot_citations_02.json",
    ]

    citations_by_key = {
        normalize_dedupe_key(item.texte): item
        for item in citation.objects.all()
    }

    for lot_path in lot_paths:
        if not lot_path.exists():
            continue

        try:
            entries = json.loads(lot_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue

        for entry in entries:
            if not isinstance(entry, dict):
                continue

            citation_item = citations_by_key.get(normalize_dedupe_key(entry.get("texte", "")))
            if not citation_item:
                continue

            citation_item.langue = entry.get("langue") or "fr"
            citation_item.theme = entry.get("theme") or "espoir"
            citation_item.verifie = entry.get("verifie", True)
            citation_item.nb_affichages = entry.get("nb_affichages", 0)
            citation_item.actif = entry.get("actif", True)
            citation_item.save(update_fields=["langue", "theme", "verifie", "nb_affichages", "actif", "date_maj"])


def noop_reverse(_apps, _schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("audits", "0002_citation_seed"),
    ]

    operations = [
        migrations.AddField(
            model_name="citation",
            name="date_maj",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="citation",
            name="langue",
            field=models.CharField(
                choices=[("fr", "Français"), ("en", "Anglais"), ("la", "Latin")],
                default="fr",
                max_length=8,
            ),
        ),
        migrations.AddField(
            model_name="citation",
            name="nb_affichages",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="citation",
            name="theme",
            field=models.CharField(
                choices=[
                    ("espoir", "Espoir"),
                    ("renouveau", "Renouveau"),
                    ("résilience", "Résilience"),
                    ("joie de vivre", "Joie de vivre"),
                    ("amour", "Amour"),
                    ("paix", "Paix"),
                ],
                default="espoir",
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name="citation",
            name="verifie",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(backfill_imported_citation_metadata, noop_reverse),
    ]
