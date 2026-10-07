from django.conf import settings
from django.db import transaction
from django.core.exceptions import PermissionDenied
from pixelprowlers.object_access import public_site_url
from pixelprowlers.notifications import safe_send_mail
from .models import Contact, ContactMessage


def open_followup(record, *, name, email, phone, service, demand, message, context):
    """Bridge published historical dossiers to the existing private ticket thread."""
    if record.followup_contact_id:
        return record.followup_contact
    contact = Contact.objects.create(name=name, email=email, phone=phone,
        service_type=service, demand_type=demand, message=message,
        request_context=context, client_dossier_id=record.client_dossier_id)
    ContactMessage.objects.create(contact=contact, author=ContactMessage.Author.CUSTOMER,
        author_name=name, message=message)
    record.followup_contact = contact
    record.save(update_fields=["followup_contact"])
    return contact


def followup_path(record):
    return f"/ticket/{record.followup_contact.secret_token}" if record.followup_contact_id else ""


def notify_client_message(message):
    contact = message.contact
    return safe_send_mail(
        event_key=f"contact-message:{message.pk}:internal",
        subject=f"[PixelProwlers] Nouveau message — {contact.ticket_id}",
        message=f"Un nouveau message attend votre traitement dans l’administration.\n{public_site_url()}/admin/crm/contact/{contact.pk}/change/",
        from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[settings.CONTACT_TO] if settings.CONTACT_TO else [])


@transaction.atomic
def reply_to_contact(*, contact, message, operator):
    if not operator.is_active or not operator.is_staff or not operator.has_perm("crm.add_contactmessage") or not operator.has_perm("crm.change_contact"):
        raise PermissionDenied
    text = message.strip()
    if not 2 <= len(text) <= 2000:
        raise ValueError("La réponse doit contenir entre 2 et 2000 caractères")
    contact = Contact.objects.select_for_update().get(pk=contact.pk)
    reply = ContactMessage.objects.create(contact=contact, message=text,
        author=ContactMessage.Author.SUPPORT, author_name=operator.get_full_name() or operator.get_username())
    contact.status = Contact.Status.WAITING_CUSTOMER
    contact.read = True
    contact.save(update_fields=["status", "read", "updated_at"])
    safe_send_mail(event_key=f"contact-message:{reply.pk}:client", subject=f"Réponse PixelProwlers — {contact.ticket_id}",
        message=f"L’atelier a répondu à votre demande.\n\nConsultez la réponse et poursuivez l’échange sur votre suivi :\n{public_site_url()}/ticket/{contact.secret_token}\n\nUne réponse à cet email ne sera pas automatiquement ajoutée au dossier.",
        from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[contact.email])
    return reply
