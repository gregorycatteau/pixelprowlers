import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from audits.models import Citation


class ImportCitationsCommandTest(TestCase):
    def test_import_is_idempotent_and_reports_invalid_entries(self):
        initial_count = Citation.objects.count()
        payload = [
            {
                "texte": "Le courage commence ici.",
                "auteur": "Anonyme",
                "source": "Test",
                "langue": "fr",
                "theme": "espoir",
                "annee": 1754,
                "ouvrage": "Carnet de test",
            },
            {
                "texte": "  le courage commence ici!  ",
                "auteur": "Anonyme",
                "source": "Test",
                "langue": "fr",
                "theme": "espoir",
                "annee": 1755,
                "metadata": {"collection": "Doublon enrichi"},
            },
            {
                "texte": "",
                "auteur": "Anonyme",
                "source": "Test",
                "langue": "fr",
                "theme": "espoir",
            },
            {
                "texte": "Un texte <script>alert(1)</script>",
                "auteur": "Anonyme",
                "source": "Test",
                "langue": "fr",
                "theme": "espoir",
            },
        ]
        fixture_path = self.tmp_path(payload)

        first_stdout = StringIO()
        call_command("import_citations", fixture_path, stdout=first_stdout)

        self.assertEqual(Citation.objects.count(), initial_count + 1)
        citation = Citation.objects.get(texte="Le courage commence ici.")
        self.assertEqual(citation.annee, 1755)
        self.assertEqual(citation.metadata["ouvrage"], "Carnet de test")
        self.assertEqual(citation.metadata["collection"], "Doublon enrichi")
        self.assertIn("Succès: 1", first_stdout.getvalue())
        self.assertIn("Doublons ignorés: 1", first_stdout.getvalue())
        self.assertIn("Erreurs de validation: 2", first_stdout.getvalue())

        second_stdout = StringIO()
        call_command("import_citations", fixture_path, stdout=second_stdout)

        self.assertEqual(Citation.objects.count(), initial_count + 1)
        self.assertIn("Succès: 0", second_stdout.getvalue())
        self.assertIn("Doublons ignorés: 2", second_stdout.getvalue())

    def tmp_path(self, payload):
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as json_file:
            json.dump(payload, json_file, ensure_ascii=False)
            return json_file.name
