from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='service_type',
            field=models.CharField(
                choices=[
                    ('audit_site', 'Audit sécurité de site web'),
                    ('site_maintenable', 'Site sobre, sécurisé, maintenable'),
                    ('maintenance_documentation', 'Maintenance, accès et documentation'),
                    ('urgence', 'Urgence : site cassé, piraté ou inaccessible'),
                    ('developpement', 'Développement Web/Applicatif'),
                    ('materiel', 'Réparation/Reconditionnement'),
                    ('formation', 'Formation & Hygiène Numérique'),
                    ('autre', 'Autre'),
                ],
                max_length=32,
            ),
        ),
    ]
