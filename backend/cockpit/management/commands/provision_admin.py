from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


GROUP_PERMISSIONS = {
    "Opérations": {
        "crm": {"view_contact", "change_contact", "view_contactmessage", "add_contactmessage"},
        "urgencies": {"view_urgencyrequest", "change_urgencyrequest"},
        "audits": {"view_clientdossier", "change_clientdossier", "view_auditdossier", "view_rdv", "change_rdv"},
    },
    "Éditorial": {
        "audits": {"view_citation", "add_citation", "change_citation", "view_motif", "change_motif", "view_raisonappel", "change_raisonappel"},
        "catalogue": {"view_refurbishedmachine", "change_refurbishedmachine", "edit_refurbishedmachine_drafts", "publish_refurbishedmachine"},
    },
    "Commercial": {
        "crm": {"view_contact", "change_contact", "view_lead", "change_lead"},
        "catalogue": {"view_refurbishedmachine", "change_refurbishedmachine", "change_refurbishedmachine_commercial_status"},
    },
    "Direction": {
        "crm": {"view_contact", "view_lead", "view_diagnosticticket"},
        "urgencies": {"view_urgencyrequest"},
        "audits": {"view_clientdossier", "view_auditdossier", "view_refonteaudit", "view_rdv"},
        "catalogue": {"view_refurbishedmachine"},
        "admin": {"view_logentry"},
    },
}


class Command(BaseCommand):
    help = "Provisionne les groupes du cockpit et un superadministrateur sans secret initial."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="striker")

    @transaction.atomic
    def handle(self, *args, **options):
        username = options["username"].strip()
        if not username or len(username) > 150:
            raise CommandError("Nom d'utilisateur invalide.")

        for group_name, app_permissions in GROUP_PERMISSIONS.items():
            group, _created = Group.objects.get_or_create(name=group_name)
            permissions = Permission.objects.none()
            for app_label, codenames in app_permissions.items():
                permissions |= Permission.objects.filter(
                    content_type__app_label=app_label,
                    codename__in=codenames,
                )
            group.permissions.set(permissions.distinct())

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(username=username)
        changed_fields = []
        for field in ("is_active", "is_staff", "is_superuser"):
            if not getattr(user, field):
                setattr(user, field, True)
                changed_fields.append(field)
        if created:
            user.set_unusable_password()
            changed_fields.append("password")
        if changed_fields:
            user.save(update_fields=changed_fields)

        state = "created_password_setup_required" if created else "verified_existing_credentials_preserved"
        self.stdout.write(self.style.SUCCESS(f"admin_account={state} groups=provisioned"))
