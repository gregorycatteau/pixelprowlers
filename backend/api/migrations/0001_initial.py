from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=160)),
                ('email', models.EmailField(max_length=254)),
                ('company', models.CharField(blank=True, max_length=180)),
                ('phone', models.CharField(blank=True, max_length=40)),
                ('service_type', models.CharField(choices=[('developpement', 'Développement Web/Applicatif'), ('materiel', 'Réparation/Reconditionnement'), ('formation', 'Formation & Hygiène Numérique'), ('autre', 'Autre')], max_length=32)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=180)),
                ('description', models.TextField()),
                ('format_type', models.CharField(choices=[('presentiel', 'Présentiel'), ('distanciel', 'Distanciel'), ('hybride', 'Hybride')], max_length=32)),
                ('duration_hours', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('max_participants', models.PositiveIntegerField(default=10)),
                ('scheduled_dates', models.JSONField(blank=True, default=list)),
                ('active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=160)),
                ('email', models.EmailField(max_length=254)),
                ('company', models.CharField(blank=True, max_length=180)),
                ('phone', models.CharField(blank=True, max_length=40)),
                ('budget', models.CharField(blank=True, max_length=80)),
                ('project_description', models.TextField()),
                ('timeline', models.CharField(blank=True, max_length=120)),
                ('lead_type', models.CharField(choices=[('developpement', 'Développement'), ('materiel', 'Matériel'), ('formation', 'Formation'), ('autre', 'Autre')], max_length=32)),
                ('status', models.CharField(choices=[('new', 'Nouveau'), ('contacted', 'Contacté'), ('qualified', 'Qualifié'), ('closed', 'Clôturé')], default='new', max_length=32)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=160)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('icon', models.CharField(blank=True, max_length=80)),
                ('service_category', models.CharField(choices=[('developpement', 'Développement'), ('materiel', 'Matériel'), ('formation', 'Formation')], max_length=32)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='FormationRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=160)),
                ('email', models.EmailField(max_length=254)),
                ('company', models.CharField(blank=True, max_length=180)),
                ('phone', models.CharField(blank=True, max_length=40)),
                ('number_of_participants', models.PositiveIntegerField(default=1)),
                ('special_needs', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'En attente'), ('confirmed', 'Confirmée'), ('cancelled', 'Annulée')], default='pending', max_length=32)),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='api.formation')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
