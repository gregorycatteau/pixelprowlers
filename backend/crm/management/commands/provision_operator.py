from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Provisionne un opérateur nominatif sans mot de passe ni privilège global."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--email", required=True)

    def handle(self, *args, **options):
        try:
            validate_email(options["email"])
        except ValidationError as exc:
            raise CommandError("Email nominatif invalide") from exc
        User = get_user_model()
        if User.objects.filter(username=options["username"]).exists():
            raise CommandError("Compte existant : examiner explicitement avant modification")
        user = User(username=options["username"], email=options["email"], first_name="Grégory", is_staff=True, is_superuser=False)
        user.set_unusable_password()
        user.save()
        models = {"crm": ["contact", "contactmessage", "notification", "diagnosticticket"],
                  "audits": ["auditdossier", "auditreponse", "refonteaudit", "rdv", "rdvcontact", "rdvrappel", "creneaucalendrier"],
                  "urgencies": ["urgencyrequest"]}
        editable = {"crm": ["contact", "notification"], "audits": ["auditdossier", "rdv", "creneaucalendrier"], "urgencies": ["urgencyrequest"]}
        for app, names in models.items():
            user.user_permissions.add(*Permission.objects.filter(content_type__app_label=app,
                content_type__model__in=names, codename__startswith="view_"))
            user.user_permissions.add(*Permission.objects.filter(content_type__app_label=app,
                content_type__model__in=editable[app], codename__startswith="change_"))
        user.user_permissions.add(Permission.objects.get(content_type__app_label="crm", codename="add_contactmessage"))
        self.stdout.write("Compte créé, mot de passe inutilisable. Le titulaire doit exécuter changepassword interactivement.")
