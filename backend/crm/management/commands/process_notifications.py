from django.core.management.base import BaseCommand, CommandError
from crm.outbox import process_one, retry
from crm.models import Notification
from django.conf import settings


class Command(BaseCommand):
    help = "Traite un lot borné de notifications privées ; aucune reprise massive des échecs."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=30)
        parser.add_argument("--id", type=int)
        parser.add_argument("--retry", type=int)
        parser.add_argument("--acknowledge-uncertain", action="store_true")
        parser.add_argument("--test-recipient", help="Recette ciblée autorisée, jamais une modification du destinataire")

    def handle(self, *args, **options):
        if not 1 <= options["limit"] <= 100:
            raise CommandError("Limite attendue entre 1 et 100")
        if options["test_recipient"]:
            if not options["id"] or options["retry"]:
                raise CommandError("La recette nécessite un unique --id sans --retry")
            item = Notification.objects.get(pk=options["id"])
            if item.recipient.lower() != options["test_recipient"].lower():
                raise CommandError("Le destinataire ne correspond pas à la boîte de recette")
            settings.NOTIFICATION_DELIVERY_ENABLED = True
            settings.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
            options["limit"] = 1
        if options["retry"]:
            try:
                retry(options["retry"], acknowledge_uncertain=options["acknowledge_uncertain"])
            except ValueError as exc:
                raise CommandError(str(exc)) from exc
            self.stdout.write("Reprise ciblée enregistrée ; aucun envoi effectué")
            return
        count = 0
        for _ in range(options["limit"]):
            if not process_one(options["id"]):
                break
            count += 1
        self.stdout.write(f"Notifications traitées : {count} ; réception à vérifier séparément")
