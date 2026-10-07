from __future__ import annotations

import base64
import json
import logging
from urllib import parse, request

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def safe_send_mail(*, subject: str, message: str, from_email: str, recipient_list: list[str], event_key: str = "") -> str:
    if event_key:
        from crm.outbox import enqueue
        return enqueue(event_key=event_key, subject=subject, message=message,
                       from_email=from_email, recipient_list=recipient_list)
    if not from_email or not recipient_list:
        return "not_configured"

    backend = settings.EMAIL_BACKEND
    smtp = backend == "django.core.mail.backends.smtp.EmailBackend"
    # In-memory backend is permitted for tests, but is never evidence of delivery.
    if not smtp and backend != "django.core.mail.backends.locmem.EmailBackend":
        return "not_configured"
    try:
        count = send_mail(subject=subject, message=message, from_email=from_email,
                          recipient_list=recipient_list, fail_silently=False)
        return ("sent" if count == 1 else "failed") if smtp else "not_configured"
    except Exception as exc:
        logger.error("Email notification failed (%s)", type(exc).__name__)
        return "failed"


def send_sms_notification(*, to: str, message: str) -> str:
    dry_run = getattr(settings, "SMS_DRY_RUN", True)
    account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
    auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
    from_number = getattr(settings, "TWILIO_FROM_NUMBER", "")

    if dry_run or not all([account_sid, auth_token, from_number, to]):
        logger.info("SMS disabled or not configured")
        return "dry_run" if to else "not_configured"

    payload = parse.urlencode({"From": from_number, "To": to, "Body": message}).encode()
    credentials = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
    endpoint = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    req = request.Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=8) as response:
            if 200 <= response.status < 300:
                return "sent"
            logger.warning("SMS provider returned status %s", response.status)
            return "failed"
    except Exception as exc:
        logger.exception("SMS notification failed: %s", exc)
        return "failed"


def send_webhook_notification(*, payload: dict, url: str = "", token: str = "") -> str:
    endpoint = url or getattr(settings, "WEBHOOK_URL", "") or getattr(settings, "URGENCY_WEBHOOK_URL", "")
    bearer = token or getattr(settings, "WEBHOOK_TOKEN", "") or getattr(settings, "URGENCY_WEBHOOK_TOKEN", "")

    if not endpoint:
        logger.info("Webhook not configured")
        return "not_configured"

    headers = {"Content-Type": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"

    req = request.Request(endpoint, data=json.dumps(payload).encode(), headers=headers, method="POST")

    try:
        with request.urlopen(req, timeout=8) as response:
            if 200 <= response.status < 300:
                return "sent"
            logger.warning("Webhook returned status %s", response.status)
            return "failed"
    except Exception as exc:
        logger.exception("Webhook notification failed: %s", exc)
        return "failed"
