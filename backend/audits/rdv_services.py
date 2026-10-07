from __future__ import annotations

from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.db import transaction, connection, IntegrityError
from django.utils import timezone

from crm.operator_services import followup_path
from pixelprowlers.object_access import public_site_url
from pixelprowlers.notifications import safe_send_mail

from .dossier_services import get_or_create_client_dossier
from .models import AuditDossier, CreneauCalendrier, Motif, RaisonAppel, Rdv, RdvContact, RdvRappel
from .models import ClientDossier


MORNING_START = time(9, 0)
MORNING_END = time(12, 30)
AFTERNOON_START = time(14, 0)
AFTERNOON_END = time(18, 0)
RESERVED_STATUSES = {
    CreneauCalendrier.Statut.RESERVE_AUDIT,
    CreneauCalendrier.Statut.RESERVE_INTERVENTION,
    CreneauCalendrier.Statut.BLOQUE,
}


def _minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def _time_from_minutes(value: int) -> time:
    return time(value // 60, value % 60)


def _period_is_free(day: date, start: time, end: time) -> bool:
    return not CreneauCalendrier.objects.filter(
        date=day,
        statut__in=RESERVED_STATUSES,
        heure_debut__lt=end,
        heure_fin__gt=start,
    ).exists()


def _day_status(day: date) -> str:
    if day.weekday() >= 5:
        return "ferme"

    day_slots = CreneauCalendrier.objects.filter(date=day)
    if day_slots.filter(statut=CreneauCalendrier.Statut.RESERVE_INTERVENTION).exists():
        return "intervention"
    if day_slots.filter(statut=CreneauCalendrier.Statut.RESERVE_AUDIT).exists():
        return "audit"

    morning_free = _period_is_free(day, MORNING_START, MORNING_END)
    afternoon_free = _period_is_free(day, AFTERNOON_START, AFTERNOON_END)
    if morning_free and afternoon_free:
        return "libre"
    if morning_free or afternoon_free:
        return "partiel"
    return "complet"


def calendar_month(year: int, month: int) -> list[dict]:
    first = date(year, month, 1)
    next_month = date(year + (month // 12), (month % 12) + 1, 1)
    total_days = (next_month - first).days

    return [
        {"date": (first + timedelta(days=index)).isoformat(), "statut": _day_status(first + timedelta(days=index))}
        for index in range(total_days)
    ]


def available_slots(motif: Motif, start_date: date, end_date: date, urgence: bool = False) -> list[dict]:
    slots = []
    current = start_date

    while current <= end_date:
        if current.weekday() < 5 or urgence:
            if motif.creneau_type == Motif.CreneauType.HORAIRE_PRECIS:
                slots.extend(_precise_slots_for_day(motif, current))
            elif motif.creneau_type == Motif.CreneauType.DEMI_JOURNEE:
                slots.extend(_half_day_slots_for_day(current))
            elif motif.creneau_type == Motif.CreneauType.JOURNEE_COMPLETE and _period_is_free(current, MORNING_START, AFTERNOON_END):
                slots.append(_slot_payload(current, MORNING_START, AFTERNOON_END, "Journée complète"))
        current += timedelta(days=1)

    return slots


def _precise_slots_for_day(motif: Motif, day: date) -> list[dict]:
    slots = []
    duration = motif.duree_minutes
    windows = [(MORNING_START, MORNING_END), (AFTERNOON_START, AFTERNOON_END)]

    for window_start, window_end in windows:
        cursor = _minutes(window_start)
        end_limit = _minutes(window_end)
        while cursor + duration <= end_limit:
            start = _time_from_minutes(cursor)
            end = _time_from_minutes(cursor + duration)
            if _period_is_free(day, start, end):
                slots.append(_slot_payload(day, start, end, f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"))
            cursor += 30

    return slots


def _half_day_slots_for_day(day: date) -> list[dict]:
    slots = []
    if _period_is_free(day, MORNING_START, MORNING_END):
        slots.append(_slot_payload(day, MORNING_START, MORNING_END, "Matinée"))
    if _period_is_free(day, AFTERNOON_START, AFTERNOON_END):
        slots.append(_slot_payload(day, AFTERNOON_START, AFTERNOON_END, "Après-midi"))
    return slots


def _slot_payload(day: date, start: time, end: time, label: str) -> dict:
    return {
        "date": day.isoformat(),
        "heure_debut": start.strftime("%H:%M"),
        "heure_fin": end.strftime("%H:%M"),
        "label": label,
    }


@transaction.atomic
def reserve_rdv(*, motif: Motif, slot: dict, contact_data: dict, raison_ids: list[int], urgence: bool, message: str = "") -> Rdv:
    day = datetime.strptime(slot["date"], "%Y-%m-%d").date()
    start = datetime.strptime(slot["heure_debut"], "%H:%M").time()
    end = datetime.strptime(slot["heure_fin"], "%H:%M").time()

    # Serialize the empty-day check too; the exclusion constraint also protects
    # direct/admin writes and overlapping (not only identical) time intervals.
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_advisory_xact_lock(%s, %s)", [816120, day.toordinal()])

    blocked = CreneauCalendrier.objects.select_for_update().filter(
        date=day,
        statut__in=RESERVED_STATUSES,
        heure_debut__lt=end,
        heure_fin__gt=start,
    )
    if blocked.exists():
        raise ValueError("Ce créneau vient d'être réservé. Merci d'en choisir un autre.")

    audit_dossier = AuditDossier.objects.filter(email__iexact=contact_data["email"]).order_by("-date_creation").first()
    client_dossier, _created = get_or_create_client_dossier(
        email=contact_data["email"],
        name=f"{contact_data['prenom']} {contact_data['nom']}",
        phone=contact_data["telephone"],
        source="rdv",
        phase=ClientDossier.Phase.PROPOSITION,
    )
    contact, _created = RdvContact.objects.update_or_create(
        email=contact_data["email"].lower(),
        defaults={
            "prenom": contact_data["prenom"],
            "nom": contact_data["nom"],
            "telephone": contact_data["telephone"],
            "audit_dossier": audit_dossier,
            "client_dossier": client_dossier,
        },
    )
    status = CreneauCalendrier.Statut.RESERVE_INTERVENTION if motif.nom.lower().find("intervention") >= 0 else CreneauCalendrier.Statut.RESERVE_AUDIT
    creneau = CreneauCalendrier.objects.create(
        date=day,
        heure_debut=start,
        heure_fin=end,
        statut=status,
        motif_reserve=motif,
        urgence=urgence,
        client=contact,
    )
    rdv = Rdv.objects.create(contact=contact, motif=motif, urgence=urgence, message=message, client_dossier=client_dossier)
    rdv.creneaux.add(creneau)
    rdv.raisons.set(RaisonAppel.objects.filter(id__in=raison_ids, actif=True))
    from crm.operator_services import open_followup
    followup = open_followup(rdv, name=f"{contact.prenom} {contact.nom}", email=contact.email, phone=contact.telephone, service="autre", demand="partnership", message=message or "Réservation de rendez-vous", context={"rdv": rdv.pk, "date": str(day), "motif": motif.nom})
    from crm.schema import _notify_contact
    _notify_contact(followup, {})
    create_reminders(rdv, day, start)
    rdv.notification_status = notify_rdv_confirmation(rdv)
    rdv.save(update_fields=["notification_status", "updated_at"])
    return rdv


def create_reminders(rdv: Rdv, day: date, start: time) -> None:
    starts_at = timezone.make_aware(datetime.combine(day, start))
    reminders = [
        (RdvRappel.TypeRappel.VEILLE, starts_at - timedelta(days=1)),
        (RdvRappel.TypeRappel.UNE_HEURE, starts_at - timedelta(hours=1)),
    ]
    for reminder_type, scheduled_at in reminders:
        RdvRappel.objects.get_or_create(rdv=rdv, type_rappel=reminder_type, defaults={"scheduled_at": scheduled_at})


def notify_rdv_confirmation(rdv: Rdv) -> dict[str, str]:
    status = {"client_email": "not_configured"}
    if not getattr(settings, "DEFAULT_FROM_EMAIL", ""):
        return status

    creneau = rdv.creneaux.order_by("date", "heure_debut").first()
    if not creneau:
        return status

    status["client_email"] = safe_send_mail(
        event_key=f"rdv:{rdv.pk}:confirmation:client",
        subject="Votre rendez-vous PixelProwlers est confirmé",
        message="\n".join([
            f"Bonjour {rdv.contact.prenom},",
            "",
            "Votre rendez-vous est confirmé.",
            f"Dossier client : {rdv.client_dossier.dossier_id if rdv.client_dossier_id else '-'}",
            f"Date : {creneau.date.strftime('%d/%m/%Y')}",
            f"Heure : {creneau.heure_debut.strftime('%H:%M')} - {creneau.heure_fin.strftime('%H:%M')}",
            f"Motif : {rdv.motif.nom}",
            "",
            "Vous recevrez un rappel la veille et 1h avant votre RDV.",
            "",
            f"Suivi et échange avec l’atelier : {public_site_url()}{followup_path(rdv)}",
                    "Répondez depuis ce suivi ; les réponses email ne sont pas automatiquement rattachées.",
                    "PixelProwlers",
        ]),
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
        recipient_list=[rdv.contact.email],
    )
    if rdv.followup_contact_id:
        contact = rdv.followup_contact
        contact.notification_status = {"client_email": status.get("client_email", "not_configured"), "client_event": f"rdv:{rdv.pk}:confirmation:client"}
        contact.save(update_fields=["notification_status"])
    return status


def send_due_reminders() -> int:
    queued = 0
    now = timezone.now()
    with transaction.atomic():
        reminders = RdvRappel.objects.select_for_update(skip_locked=True, of=("self",)).select_related("rdv__contact").filter(status="pending", scheduled_at__lte=now)
        for reminder in reminders:
            if reminder.rdv.statut == Rdv.Statut.ANNULE:
                reminder.status = "cancelled"
            elif notify_rdv_reminder(reminder) == "pending":
                reminder.status = "queued"
                queued += 1
            else:
                continue
            reminder.save(update_fields=["status"])
    return queued


def notify_rdv_reminder(reminder: RdvRappel) -> str:
    if not getattr(settings, "DEFAULT_FROM_EMAIL", ""):
        return
    creneau = reminder.rdv.creneaux.order_by("date", "heure_debut").first()
    if not creneau:
        return
    status = safe_send_mail(
        event_key=f"rdv-reminder:{reminder.pk}:client",
        subject="Rappel de votre rendez-vous PixelProwlers",
        message="\n".join([
            f"Bonjour {reminder.rdv.contact.prenom},",
            "",
            f"Petit rappel : votre rendez-vous PixelProwlers est prévu le {creneau.date.strftime('%d/%m/%Y')} à {creneau.heure_debut.strftime('%H:%M')}.",
            f"Motif : {reminder.rdv.motif.nom}",
            "",
            "À bientôt.",
        ]),
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
        recipient_list=[reminder.rdv.contact.email],
    )
    return status
