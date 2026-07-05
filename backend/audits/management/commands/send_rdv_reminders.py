from django.core.management.base import BaseCommand

from audits.rdv_services import send_due_reminders


class Command(BaseCommand):
    help = "Envoie les rappels RDV échus. À lancer par cron toutes les 5 à 15 minutes."

    def handle(self, *args, **options):
        sent = send_due_reminders()
        self.stdout.write(self.style.SUCCESS(f"Rappels RDV envoyés: {sent}"))
