from __future__ import annotations

from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import AuditDossier, CreneauCalendrier, Motif, RaisonAppel, Rdv, RdvContact, RdvRappel


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

    blocked = CreneauCalendrier.objects.select_for_update().filter(
        date=day,
        statut__in=RESERVED_STATUSES,
        heure_debut__lt=end,
        heure_fin__gt=start,
    )
    if blocked.exists():
        raise ValueError("Ce créneau vient d'être réservé. Merci d'en choisir un autre.")

    audit_dossier = AuditDossier.objects.filter(email__iexact=contact_data["email"]).order_by("-date_creation").first()
    contact, _created = RdvContact.objects.update_or_create(
        email=contact_data["email"].lower(),
        defaults={
            "prenom": contact_data["prenom"],
            "nom": contact_data["nom"],
            "telephone": contact_data["telephone"],
            "audit_dossier": audit_dossier,
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
    rdv = Rdv.objects.create(contact=contact, motif=motif, urgence=urgence, message=message)
    rdv.creneaux.add(creneau)
    rdv.raisons.set(RaisonAppel.objects.filter(id__in=raison_ids, actif=True))
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

    try:
        send_mail(
            subject="Votre rendez-vous PixelProwlers est confirmé",
            message="\n".join([
                f"Bonjour {rdv.contact.prenom},",
                "",
                "Votre rendez-vous est confirmé.",
                f"Date : {creneau.date.strftime('%d/%m/%Y')}",
                f"Heure : {creneau.heure_debut.strftime('%H:%M')} - {creneau.heure_fin.strftime('%H:%M')}",
                f"Motif : {rdv.motif.nom}",
                "",
                "Vous recevrez un rappel la veille et 1h avant votre RDV.",
                "",
                "PixelProwlers",
            ]),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
            recipient_list=[rdv.contact.email],
            fail_silently=False,
        )
        status["client_email"] = "sent"
    except Exception:
        status["client_email"] = "failed"
    return status


def send_due_reminders() -> int:
    sent = 0
    now = timezone.now()
    for reminder in RdvRappel.objects.select_related("rdv__contact").filter(status="pending", scheduled_at__lte=now):
        try:
            notify_rdv_reminder(reminder)
            reminder.status = "sent"
            reminder.sent_at = now
            reminder.last_error = ""
            reminder.save(update_fields=["status", "sent_at", "last_error"])
            sent += 1
        except Exception as exc:
            reminder.status = "failed"
            reminder.last_error = str(exc)[:500]
            reminder.save(update_fields=["status", "last_error"])
    return sent


def notify_rdv_reminder(reminder: RdvRappel) -> None:
    if not getattr(settings, "DEFAULT_FROM_EMAIL", ""):
        return
    creneau = reminder.rdv.creneaux.order_by("date", "heure_debut").first()
    if not creneau:
        return
    send_mail(
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
        fail_silently=False,
    )
