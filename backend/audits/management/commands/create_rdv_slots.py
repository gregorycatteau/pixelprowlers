from datetime import date, timedelta, time

from django.core.management.base import BaseCommand

from audits.models import CreneauCalendrier


class Command(BaseCommand):
    help = "Crée des créneaux RDV libres standards sur une période ouvrée."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=14)

    def handle(self, *args, **options):
        created = 0
        today = date.today()
        for day_offset in range(options["days"]):
            current = today + timedelta(days=day_offset)
            if current.weekday() >= 5:
                continue
            for start, end in [(time(9, 0), time(12, 30)), (time(14, 0), time(18, 0))]:
                _slot, was_created = CreneauCalendrier.objects.get_or_create(
                    date=current,
                    heure_debut=start,
                    heure_fin=end,
                    defaults={"statut": CreneauCalendrier.Statut.LIBRE},
                )
                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Créneaux créés: {created}"))
