"""
Importe un lot de citations depuis un fichier JSON UTF-8.

Usage:
    python manage.py import_citations chemin/vers/citations.json

Format attendu:
    [
      {
        "texte": "Le texte de la citation.",
        "auteur": "Nom de l'auteur",
        "source": "Obligatoire",
        "langue": "fr",
        "theme": "espoir",
        "annee": 1754,
        "metadata": {"ouvrage": "Optionnel"},
        "actif": true,
        "verifie": true,
        "nb_affichages": 0
      }
    ]
"""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models import Max

from audits.models import Citation


ALLOWED_LANGUAGES = {"fr", "en", "la"}
ALLOWED_THEMES = {"espoir", "renouveau", "résilience", "joie de vivre", "amour", "paix"}
OPTIONAL_FIELD_DEFAULTS = {
    "langue": "fr",
    "theme": "espoir",
    "actif": True,
    "verifie": True,
    "nb_affichages": 0,
}
KNOWN_FIELDS = {"texte", "auteur", "source", "langue", "theme", "actif", "verifie", "nb_affichages", "annee", "année", "year", "metadata"}

CONTROL_CHARACTERS_PATTERN = re.compile(r"[\u0000-\u001F\u007F-\u009F\u200B-\u200D\uFEFF]")
HTML_PATTERN = re.compile(r"[<>]")
INJECTION_PATTERN = re.compile(r"(--|/\*|\*/|`|\$\{)")
MULTIPLE_SPACES_PATTERN = re.compile(r"\s+")
FINAL_PUNCTUATION_PATTERN = re.compile(r"[\s\.,;:!?…\"'»”’\)\]]+$")


def normalize_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""

    normalized = unicodedata.normalize("NFC", value)
    normalized = MULTIPLE_SPACES_PATTERN.sub(" ", normalized)
    return normalized.strip()


def normalize_dedupe_key(value: str) -> str:
    return FINAL_PUNCTUATION_PATTERN.sub("", normalize_text(value)).casefold()


def validate_safe_text(value: str, field_name: str) -> list[str]:
    errors = []

    if CONTROL_CHARACTERS_PATTERN.search(value):
        errors.append(f"{field_name}: caractères de contrôle interdits")
    if HTML_PATTERN.search(value):
        errors.append(f"{field_name}: balises HTML ou chevrons interdits")
    if INJECTION_PATTERN.search(value):
        errors.append(f"{field_name}: séquences d'injection interdites")

    return errors


def sanitize_metadata_value(value: Any) -> Any:
    if isinstance(value, str):
        return normalize_text(value)
    if isinstance(value, dict):
        return {str(key): sanitize_metadata_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_metadata_value(item) for item in value]
    if value is None or isinstance(value, (bool, int, float)):
        return value

    return str(value)


def validate_metadata(value: Any, field_name: str) -> list[str]:
    errors: list[str] = []

    if isinstance(value, str):
        errors.extend(validate_safe_text(value, field_name))
    elif isinstance(value, dict):
        for key, item in value.items():
            errors.extend(validate_safe_text(str(key), f"{field_name}.{key}"))
            errors.extend(validate_metadata(item, f"{field_name}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(validate_metadata(item, f"{field_name}[{index}]"))

    return errors


class ImportLogger:
    def __init__(self) -> None:
        log_dir = Path(settings.BASE_DIR) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("audits.import_citations")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        log_path = log_dir / "import_citations.log"
        if not any(isinstance(handler, logging.FileHandler) and Path(handler.baseFilename) == log_path for handler in self.logger.handlers):
            handler = logging.FileHandler(log_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            self.logger.addHandler(handler)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)


class Command(BaseCommand):
    help = "Importe des citations depuis un fichier JSON UTF-8 avec validation, déduplication et journalisation."

    def add_arguments(self, parser) -> None:
        parser.add_argument("json_file", type=str, help="Chemin vers le fichier JSON à importer.")

    def handle(self, *args, **options) -> None:
        json_path = Path(options["json_file"])
        import_logger = ImportLogger()

        connection.ensure_connection()
        if connection.vendor != "postgresql":
            raise CommandError("Import refusé: la base active doit être PostgreSQL.")

        if not json_path.exists() or not json_path.is_file():
            raise CommandError(f"Fichier introuvable: {json_path}")

        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(f"JSON invalide dans {json_path}: {exc}") from exc

        if not isinstance(payload, list):
            raise CommandError("Le fichier JSON doit contenir une liste d'objets.")

        model_fields = {field.name for field in Citation._meta.get_fields()}
        existing_by_key = {
            normalize_dedupe_key(citation.texte): citation
            for citation in Citation.objects.all()
        }

        imported_count = 0
        duplicate_count = 0
        validation_errors: list[str] = []

        import_logger.info(f"Début import citations: {json_path}")

        for index, raw_entry in enumerate(payload, start=1):
            entry_label = f"entrée #{index}"

            if not isinstance(raw_entry, dict):
                message = f"{entry_label}: objet JSON attendu"
                validation_errors.append(message)
                import_logger.error(message)
                continue

            cleaned, errors = self.validate_entry(raw_entry, entry_label)
            if errors:
                validation_errors.extend(errors)
                for error in errors:
                    import_logger.error(error)
                continue

            dedupe_key = normalize_dedupe_key(cleaned["texte"])
            if dedupe_key in existing_by_key:
                duplicate_count += 1
                updated_fields = self.update_existing_metadata(existing_by_key[dedupe_key], cleaned, model_fields)
                message = f"{entry_label}: doublon ignoré ({cleaned['texte'][:80]})"
                if updated_fields:
                    message = f"{message}; métadonnées mises à jour: {', '.join(updated_fields)}"
                self.stdout.write(self.style.WARNING(message))
                import_logger.warning(message)
                continue

            create_values = {field_name: value for field_name, value in cleaned.items() if field_name in model_fields}
            if "numero" in model_fields:
                create_values["numero"] = self.next_citation_number()
            ignored_fields = sorted(set(cleaned) - set(create_values))
            if ignored_fields:
                import_logger.warning(
                    f"{entry_label}: champs ignorés car absents du modèle Citation: {', '.join(ignored_fields)}"
                )

            citation = Citation.objects.create(**create_values)
            existing_by_key[dedupe_key] = citation
            imported_count += 1
            import_logger.info(f"{entry_label}: citation importée ({cleaned['texte'][:80]})")

        summary_lines = [
            "Import citations terminé.",
            f"Succès: {imported_count}",
            f"Doublons ignorés: {duplicate_count}",
            f"Erreurs de validation: {len(validation_errors)}",
        ]

        self.stdout.write(self.style.SUCCESS(summary_lines[0]))
        for line in summary_lines[1:]:
            self.stdout.write(line)
            import_logger.info(line)

        if validation_errors:
            self.stdout.write(self.style.ERROR("Détail des erreurs:"))
            import_logger.error("Détail des erreurs:")
            for error in validation_errors:
                self.stdout.write(self.style.ERROR(f"- {error}"))
                import_logger.error(error)

    def validate_entry(self, entry: dict[str, Any], entry_label: str) -> tuple[dict[str, Any], list[str]]:
        errors: list[str] = []
        cleaned: dict[str, Any] = {}

        texte = normalize_text(entry.get("texte"))
        auteur = normalize_text(entry.get("auteur"))
        source = normalize_text(entry.get("source"))
        langue = normalize_text(entry.get("langue", OPTIONAL_FIELD_DEFAULTS["langue"])).casefold()
        theme = normalize_text(entry.get("theme", OPTIONAL_FIELD_DEFAULTS["theme"])).casefold()

        if not texte:
            errors.append(f"{entry_label}: texte obligatoire manquant")
        if not auteur:
            errors.append(f"{entry_label}: auteur obligatoire manquant")
        if not source:
            errors.append(f"{entry_label}: source obligatoire manquante")

        for field_name, value in {"texte": texte, "auteur": auteur, "source": source}.items():
            if value:
                errors.extend(f"{entry_label}: {error}" for error in validate_safe_text(value, field_name))

        if langue not in ALLOWED_LANGUAGES:
            errors.append(f"{entry_label}: langue invalide '{langue}' (valeurs: {', '.join(sorted(ALLOWED_LANGUAGES))})")

        if theme not in ALLOWED_THEMES:
            errors.append(f"{entry_label}: thème invalide '{theme}' (valeurs: {', '.join(sorted(ALLOWED_THEMES))})")

        actif = entry.get("actif", OPTIONAL_FIELD_DEFAULTS["actif"])
        verifie = entry.get("verifie", OPTIONAL_FIELD_DEFAULTS["verifie"])
        nb_affichages = entry.get("nb_affichages", OPTIONAL_FIELD_DEFAULTS["nb_affichages"])
        annee = entry.get("annee", entry.get("année", entry.get("year")))
        metadata = entry.get("metadata", {})
        extra_metadata = {
            key: value
            for key, value in entry.items()
            if key not in KNOWN_FIELDS
        }

        if not isinstance(actif, bool):
            errors.append(f"{entry_label}: actif doit être un booléen")
        if not isinstance(verifie, bool):
            errors.append(f"{entry_label}: verifie doit être un booléen")
        if not isinstance(nb_affichages, int) or nb_affichages < 0:
            errors.append(f"{entry_label}: nb_affichages doit être un entier positif ou nul")
        if annee is not None and (not isinstance(annee, int) or annee < 0 or annee > 9999):
            errors.append(f"{entry_label}: annee doit être un entier entre 0 et 9999")
        if not isinstance(metadata, dict):
            errors.append(f"{entry_label}: metadata doit être un objet JSON")

        metadata_errors = validate_metadata(metadata, "metadata") + validate_metadata(extra_metadata, "metadata_extra")
        errors.extend(f"{entry_label}: {error}" for error in metadata_errors)

        if errors:
            return {}, errors

        merged_metadata = {
            **sanitize_metadata_value(metadata),
            **sanitize_metadata_value(extra_metadata),
        }

        cleaned.update(
            texte=texte,
            auteur=auteur,
            source=source,
            langue=langue,
            theme=theme,
            actif=actif,
            verifie=verifie,
            nb_affichages=nb_affichages,
            annee=annee,
            metadata=merged_metadata,
        )
        return cleaned, []

    def next_citation_number(self) -> int:
        return (Citation.objects.aggregate(max_numero=Max("numero"))["max_numero"] or 0) + 1

    def update_existing_metadata(self, citation: Citation, cleaned: dict[str, Any], model_fields: set[str]) -> list[str]:
        updatable_fields = [
            "source",
            "langue",
            "theme",
            "actif",
            "verifie",
            "nb_affichages",
            "annee",
        ]
        updated_fields: list[str] = []

        for field_name in updatable_fields:
            if field_name not in model_fields or field_name not in cleaned:
                continue
            if field_name == "annee" and cleaned[field_name] is None:
                continue
            if getattr(citation, field_name) != cleaned[field_name]:
                setattr(citation, field_name, cleaned[field_name])
                updated_fields.append(field_name)

        if "metadata" in model_fields and cleaned.get("metadata"):
            merged_metadata = {
                **(citation.metadata or {}),
                **cleaned["metadata"],
            }
            if merged_metadata != (citation.metadata or {}):
                citation.metadata = merged_metadata
                updated_fields.append("metadata")

        if updated_fields:
            citation.save(update_fields=[*updated_fields, "date_maj"])

        return updated_fields
