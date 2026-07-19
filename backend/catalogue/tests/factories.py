from catalogue.models import RefurbishedMachine


def machine_data(reference="CAT-001", slug="machine-001", **overrides):
    data = {
        "internal_reference": reference,
        "slug": slug,
        "title": "ThinkPad reconditionné",
        "brand": "Lenovo",
        "model_name": "ThinkPad T480",
        "summary": "Portable professionnel testé et reconditionné.",
        "description": "Machine nettoyée, contrôlée et prête à l'emploi.",
        "cosmetic_condition": "Bon état, traces d'usage normales.",
        "installed_operating_system": "Debian GNU/Linux 13",
        "specifications": [{"name": "Mémoire", "value": "16 Go"}],
        "performed_interventions": [{"name": "Nettoyage", "value": "Interne et externe"}],
        "performed_tests": [{"name": "Mémoire", "value": "Test réussi"}],
    }
    data.update(overrides)
    return data


def create_machine(reference="CAT-001", slug="machine-001", **overrides):
    return RefurbishedMachine.objects.create(**machine_data(reference, slug, **overrides))
