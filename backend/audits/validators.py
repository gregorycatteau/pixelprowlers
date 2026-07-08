"""
Fonctions de validation réutilisables pour les mutations GraphQL.
Utilisées par les mutations GraphQL (audits/mutations.py) pour valider les inputs
avant création/modification des objets métier.
"""
from datetime import datetime

from .models import Motif, RaisonAppel


def validate_motif(motif_id):
    try:
        return Motif.objects.get(id=int(motif_id), actif=True)
    except (ValueError, TypeError, Motif.DoesNotExist):
        raise ValueError("Motif invalide ou introuvable.")


def validate_raison_appel(raison_id):
    try:
        return RaisonAppel.objects.get(id=int(raison_id), actif=True)
    except (ValueError, TypeError, RaisonAppel.DoesNotExist):
        raise ValueError("Raison d'appel invalide ou introuvable.")


def validate_date_range(date_debut, date_fin):
    try:
        start_date = datetime.strptime(date_debut, "%Y-%m-%d").date()
        end_date = datetime.strptime(date_fin, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError("Format de date invalide (attendu: YYYY-MM-DD).")

    if end_date < start_date:
        raise ValueError("date_fin doit être postérieure ou égale à date_debut.")

    return start_date, end_date


def validate_year_month(annee, mois):
    try:
        year = int(annee)
        month = int(mois)
        if month < 1 or month > 12:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("annee et mois sont obligatoires et valides.")

    return year, month


def validate_email_format(email):
    import re
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not email or not re.match(pattern, email):
        raise ValueError("Adresse email invalide.")
    return email
