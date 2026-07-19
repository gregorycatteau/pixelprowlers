import re
from decimal import Decimal

from django.core.exceptions import ValidationError


MAX_JSON_ENTRIES = 50
MAX_JSON_NAME_LENGTH = 80
MAX_JSON_VALUE_LENGTH = 500
_HTML_TAG = re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>")


def validate_plain_text(value):
    if value and _HTML_TAG.search(value):
        raise ValidationError("Le HTML n'est pas autorisé.")


def validate_structured_entries(value):
    if not isinstance(value, list):
        raise ValidationError("Une liste d'entrées structurées est requise.")
    if len(value) > MAX_JSON_ENTRIES:
        raise ValidationError(f"La liste ne peut pas dépasser {MAX_JSON_ENTRIES} entrées.")

    for index, entry in enumerate(value):
        if not isinstance(entry, dict) or set(entry) - {"name", "value"}:
            raise ValidationError(
                f"L'entrée {index + 1} doit contenir uniquement name et, facultativement, value."
            )
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip() or len(name) > MAX_JSON_NAME_LENGTH:
            raise ValidationError(f"Le nom de l'entrée {index + 1} est invalide.")
        validate_plain_text(name)

        item_value = entry.get("value", "")
        if isinstance(item_value, bool):
            continue
        if isinstance(item_value, (int, float, Decimal)) and not isinstance(item_value, complex):
            continue
        if not isinstance(item_value, str) or len(item_value) > MAX_JSON_VALUE_LENGTH:
            raise ValidationError(f"La valeur de l'entrée {index + 1} est invalide.")
        validate_plain_text(item_value)
