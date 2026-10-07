"""Durable private SMTP submission, with conservative ambiguity handling."""
import hashlib
import smtplib
import socket
from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.utils import timezone

from .models import Notification

MAX_ATTEMPTS = 5
LEASE_SECONDS = 120


def enqueue(*, event_key, subject, message, from_email, recipient_list):
    if not recipient_list or not from_email:
        return "not_configured"
    with transaction.atomic():
        for recipient in recipient_list:
            digest = hashlib.sha256(recipient.lower().encode()).hexdigest()[:32]
            Notification.objects.get_or_create(
                event_key=f"{event_key}:{digest}",
                defaults={"recipient": recipient, "subject": subject, "body": message,
                          "sender": from_email, "reply_to": settings.NOTIFICATION_REPLY_TO},
            )
    return "pending"


def claim(notification_id=None):
    now = timezone.now()
    with transaction.atomic():
        # A process may have died after DATA acceptance. Never blindly replay it.
        Notification.objects.filter(state=Notification.State.SENDING, lease_until__lte=now).update(
            state=Notification.State.UNCERTAIN, lease_until=None, last_error="worker_interrupted")
        query = Notification.objects.select_for_update(skip_locked=True).filter(
            state__in=[Notification.State.PENDING, Notification.State.TEMPORARY], next_attempt_at__lte=now)
        if notification_id is not None:
            query = query.filter(pk=notification_id)
        item = query.first()
        if item is None:
            return None
        item.state = Notification.State.SENDING
        item.attempts += 1
        item.lease_until = now + timedelta(seconds=LEASE_SECONDS)
        item.save(update_fields=["state", "attempts", "lease_until", "updated_at"])
        return item


def process_one(notification_id=None):
    # No connection, console body or simulation is ever a production submission.
    if not settings.NOTIFICATION_DELIVERY_ENABLED:
        return False
    if (settings.EMAIL_BACKEND != "django.core.mail.backends.smtp.EmailBackend"
            or settings.EMAIL_USE_TLS == settings.EMAIL_USE_SSL
            or not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD
            or not settings.EMAIL_TIMEOUT or settings.EMAIL_TIMEOUT > 60):
        raise RuntimeError("SMTP sécurisé authentifié avec timeout requis")
    item = claim(notification_id)
    if item is None:
        return False
    state, error = Notification.State.ACCEPTED, ""
    try:
        count = EmailMessage(item.subject, item.body, item.sender, [item.recipient],
                             reply_to=[item.reply_to] if item.reply_to else [],
                             headers={"Message-ID": f"<pixelprowlers-{item.pk}@pixelprowlers.io>"}).send(fail_silently=False)
        if count != 1:
            state, error = Notification.State.TEMPORARY, "relay_did_not_accept"
    except smtplib.SMTPRecipientsRefused as exc:
        codes = [detail[0] for detail in exc.recipients.values()]
        state = Notification.State.TEMPORARY if any(400 <= c < 500 for c in codes) else Notification.State.PERMANENT
        error = "SMTPRecipientsRefused"
    except smtplib.SMTPResponseException as exc:
        state = Notification.State.TEMPORARY if 400 <= exc.smtp_code < 500 else Notification.State.PERMANENT
        error = type(exc).__name__
    except (ConnectionRefusedError, socket.gaierror) as exc:
        state, error = Notification.State.TEMPORARY, type(exc).__name__
    except Exception as exc:
        # Timeout, disconnect or unknown error may occur after remote acceptance.
        state, error = Notification.State.UNCERTAIN, type(exc).__name__
    if state == Notification.State.TEMPORARY and item.attempts >= MAX_ATTEMPTS:
        state = Notification.State.PERMANENT
    now = timezone.now()
    Notification.objects.filter(pk=item.pk, state=Notification.State.SENDING, attempts=item.attempts).update(
        state=state, last_error=error, lease_until=None,
        next_attempt_at=now + timedelta(seconds=min(3600, 60 * 2 ** (item.attempts - 1))),
        accepted_at=now if state == Notification.State.ACCEPTED else None, updated_at=now)
    return True


def retry(notification_id, *, acknowledge_uncertain=False):
    with transaction.atomic():
        item = Notification.objects.select_for_update().get(pk=notification_id)
        allowed = [Notification.State.TEMPORARY, Notification.State.PERMANENT]
        if acknowledge_uncertain:
            allowed.append(Notification.State.UNCERTAIN)
        if item.state not in allowed:
            raise ValueError("Reprise refusée : vérifier le relais et reconnaître une éventuelle duplication")
        item.state = Notification.State.PENDING
        item.next_attempt_at = timezone.now()
        item.last_error = "operator_retry"
        item.save(update_fields=["state", "next_attempt_at", "last_error", "updated_at"])
