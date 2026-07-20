from datetime import timedelta

from django import template
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils import timezone

from audits.models import AuditDossier, CreneauCalendrier, Rdv
from catalogue.models import RefurbishedMachine
from crm.models import Contact
from urgencies.models import UrgencyRequest


register = template.Library()


def _metric(label, value, url, tone="info"):
    return {"label": label, "value": value, "url": url, "tone": tone}


@register.simple_tag
def cockpit_dashboard(user, app_list):
    today = timezone.localdate()
    recent_cutoff = timezone.now() - timedelta(days=7)
    metrics = []
    visible_apps = {app["app_label"] for app in app_list}

    if "crm" in visible_apps:
        contact_url = reverse("admin:crm_contact_changelist")
        metrics.extend(
            [
                _metric("Nouveaux contacts (7 j)", Contact.objects.filter(created_at__gte=recent_cutoff).count(), f"{contact_url}?created_at__gte={recent_cutoff.date().isoformat()}"),
                _metric("Contacts non traités", Contact.objects.exclude(status__in=[Contact.Status.RESOLVED, Contact.Status.CLOSED]).count(), f"{contact_url}?status__exact={Contact.Status.OPEN}", "warning"),
                _metric("Notifications en échec", Contact.objects.filter(statut_notification=Contact.NotificationStatus.FAILED).count(), f"{contact_url}?statut_notification__exact={Contact.NotificationStatus.FAILED}", "danger"),
            ]
        )

    if "urgencies" in visible_apps:
        urgency_url = reverse("admin:urgencies_urgencyrequest_changelist")
        metrics.append(_metric("Urgences ouvertes", UrgencyRequest.objects.filter(status="open").count(), f"{urgency_url}?status__exact=open", "danger"))

    if "audits" in visible_apps:
        rdv_url = reverse("admin:audits_rdv_changelist")
        metrics.append(
            _metric(
                "Rendez-vous à venir",
                Rdv.objects.filter(statut=Rdv.Statut.CONFIRME, creneaux__date__gte=today).distinct().count(),
                f"{rdv_url}?statut__exact={Rdv.Statut.CONFIRME}",
            )
        )

    if "audits" in visible_apps:
        audit_url = reverse("admin:audits_auditdossier_changelist")
        metrics.append(_metric("Dossiers d'audit", AuditDossier.objects.count(), audit_url))

    if "catalogue" in visible_apps:
        machine_url = reverse("admin:catalogue_refurbishedmachine_changelist")
        for label, status, tone in (
            ("Machines disponibles", RefurbishedMachine.CommercialStatus.AVAILABLE, "success"),
            ("Machines réservées", RefurbishedMachine.CommercialStatus.RESERVED, "warning"),
            ("Machines vendues", RefurbishedMachine.CommercialStatus.SOLD, "info"),
        ):
            metrics.append(_metric(label, RefurbishedMachine.objects.filter(commercial_status=status).count(), f"{machine_url}?commercial_status__exact={status}", tone))
        metrics.append(_metric("Brouillons à publier", RefurbishedMachine.objects.filter(status=RefurbishedMachine.Status.DRAFT).count(), f"{machine_url}?status__exact={RefurbishedMachine.Status.DRAFT}", "warning"))

    recent_actions = []
    if user.is_superuser or user.has_perm("admin.view_logentry"):
        recent_actions = LogEntry.objects.select_related("user", "content_type")[:8]

    return {"metrics": metrics, "recent_actions": recent_actions}
