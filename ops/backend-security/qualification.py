import os,sys,socket
if os.getenv("QUAL_DB_HOST", "pixelprowlers-security-db-20261006") not in {"pixelprowlers-security-db-20261006", "pixelprowlers-security-restore-20261006"}:
    raise RuntimeError("Only dedicated qualification databases are allowed")
if os.getenv("QUAL_DB_USER", "qualification_owner") not in {"qualification_owner", "pixelprowlers_app"}:
    raise RuntimeError("Unknown qualification account")
sys.path.insert(0,os.getenv("QUAL_SOURCE", "/app"))
os.environ.update(DJANGO_SETTINGS_MODULE="pixelprowlers.settings",DJANGO_DEBUG="True",POSTGRES_PASSWORD="qualification-only-not-production",DJANGO_SECRET_KEY="synthetic-django-qualification-only-not-production")
from django.conf import settings
settings.DATABASES={"default":{"ENGINE":"django.db.backends.postgresql","HOST":os.getenv("QUAL_DB_HOST","pixelprowlers-security-db-20261006"),"PORT":"5432","NAME":"qualification_only","USER":os.getenv("QUAL_DB_USER","qualification_owner"),"PASSWORD":"qualification-only-not-production"}}
settings.AUDIT_SIGNATURE_KEY="synthetic-qualification-only-not-production"
settings.SECRET_KEY="synthetic-django-qualification-only-not-production"
settings.EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
settings.DEFAULT_FROM_EMAIL="qualification@example.invalid"
settings.CONTACT_TO=settings.AUDIT_INTERNAL_EMAIL=settings.URGENCY_INTERNAL_EMAIL="qualification@example.invalid"
settings.SMS_DRY_RUN=True
settings.WEBHOOK_URL=settings.URGENCY_WEBHOOK_URL=""
settings.ALLOWED_HOSTS=["testserver","localhost","127.0.0.1"]
settings.CORS_ALLOWED_ORIGINS=["http://localhost","http://localhost:3000","http://127.0.0.1:3520"]
settings.SECURE_SSL_REDIRECT=False
settings.SESSION_COOKIE_SECURE=False
settings.DEBUG=os.getenv("QUAL_DEBUG","True")=="True"
import django
django.setup()
from django.core.management import call_command
args=sys.argv[1:]
if args==["serve"]:call_command("runserver","0.0.0.0:8000",use_reloader=False,verbosity=0)
else:call_command(*args,interactive=False) if args[0] in ["test","migrate"] else call_command(*args)
