import os
import logging
from email.utils import parseaddr
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured
from django.core.validators import validate_email

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent
DEV_INSECURE_SECRET_KEY = "pixelprowlers-dev-insecure-change-me"
logger = logging.getLogger(__name__)


def load_env_file() -> None:
    env_paths = (PROJECT_DIR / ".env", BASE_DIR / ".env")

    for env_path in env_paths:
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key:
                os.environ.setdefault(key, value)


load_env_file()


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def env_first(*names: str, default: str = "") -> str:
    for name in names:
        value = env(name)
        if value:
            return value

    return default


def env_bool(name: str, default: bool = False) -> bool:
    value = env(name)

    if not value:
        return default

    return value.lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    raw = env(name, default=default)
    return [item.strip() for item in raw.split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", env_bool("DEBUG", True))
SECRET_KEY = env("DJANGO_SECRET_KEY")

if not SECRET_KEY and DEBUG:
    SECRET_KEY = DEV_INSECURE_SECRET_KEY
    logger.warning(
        "DJANGO_SECRET_KEY is not set. Using local development fallback SECRET_KEY; "
        "this must never be used with DJANGO_DEBUG=False."
    )

if not DEBUG and not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production.")

ALLOWED_HOSTS = [
    host.strip()
    for host in env_first("DJANGO_ALLOWED_HOSTS", "ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "cockpit",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "graphene_django",
    "audits",
    "catalogue",
    "crm",
    "urgencies",
    "tracking",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pixelprowlers.urls"
WSGI_APPLICATION = "pixelprowlers.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


def database_config():
    database_url = env("DATABASE_URL")

    if database_url:
        parsed = urlparse(database_url)

        if parsed.scheme not in {"postgres", "postgresql"}:
            raise ValueError("DATABASE_URL doit utiliser postgres:// ou postgresql://.")

        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "",
            "PORT": str(parsed.port or ""),
        }

    password = env_first("POSTGRES_PASSWORD", "DB_PASSWORD")
    if not password:
        raise ValueError("Configuration PostgreSQL incomplète: POSTGRES_PASSWORD ou DB_PASSWORD est obligatoire.")

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env_first("POSTGRES_DB", "DB_NAME", default="pixelprowlers"),
        "USER": env_first("POSTGRES_USER", "DB_USER", default="pixelprowlers"),
        "PASSWORD": password,
        "HOST": env_first("POSTGRES_HOST", "DB_HOST", default="127.0.0.1"),
        "PORT": env_first("POSTGRES_PORT", "DB_PORT", default="5433"),
    }


DATABASES = {
    "default": database_config(),
}

GRAPHENE = {
    "SCHEMA": "pixelprowlers.schema.schema",
}

# CORS strict: only explicit frontend origins are allowed.
# Production values come from the repo deployment docs.
CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,https://pixelprowlers.io,https://www.pixelprowlers.io",
)
CORS_ALLOW_CREDENTIALS = env_bool("CORS_ALLOW_CREDENTIALS", False)

CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,https://pixelprowlers.io,https://www.pixelprowlers.io",
)
USE_X_FORWARDED_HOST = env_bool("DJANGO_USE_X_FORWARDED_HOST", True)

if DEBUG:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", False)
    SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", False)
    CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", False)
    SECURE_HSTS_SECONDS = int(env("DJANGO_SECURE_HSTS_SECONDS", "0") or "0")
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
    SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)
else:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = int(env("DJANGO_ADMIN_SESSION_AGE", "28800") or "28800")
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# Explicit upper bound for request bodies parsed by Django. Caddy should apply
# an equal or smaller limit at the public edge.
DATA_UPLOAD_MAX_MEMORY_SIZE = int(env("DJANGO_MAX_REQUEST_BODY_BYTES", "1048576") or "1048576")

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


def warn_email_alias_conflict(canonical: str, legacy: str, *, boolean: bool = False) -> None:
    canonical_value = env(canonical)
    legacy_value = env(legacy)
    if not canonical_value or not legacy_value:
        return
    if boolean:
        conflicts = env_bool(canonical) != env_bool(legacy)
    else:
        conflicts = canonical_value != legacy_value
    if conflicts:
        logger.warning(
            "email_configuration_conflict canonical=%s legacy=%s action=canonical_wins",
            canonical,
            legacy,
        )


for canonical_name, legacy_name, is_boolean in (
    ("EMAIL_HOST", "SMTP_HOST", False),
    ("EMAIL_PORT", "SMTP_PORT", False),
    ("EMAIL_HOST_USER", "SMTP_USER", False),
    ("EMAIL_HOST_PASSWORD", "SMTP_PASS", False),
    ("EMAIL_USE_TLS", "SMTP_USE_TLS", True),
    ("EMAIL_USE_TLS", "SMTP_SECURE", True),
):
    warn_email_alias_conflict(canonical_name, legacy_name, boolean=is_boolean)


EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
    if env_first("EMAIL_HOST", "SMTP_HOST")
    else "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = env_first("EMAIL_HOST", "SMTP_HOST", default="localhost")
EMAIL_PORT = int(env_first("EMAIL_PORT", "SMTP_PORT", default="25") or "25")
EMAIL_HOST_USER = env_first("EMAIL_HOST_USER", "SMTP_USER")
EMAIL_HOST_PASSWORD = env_first("EMAIL_HOST_PASSWORD", "SMTP_PASS")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", env_bool("SMTP_USE_TLS", env_bool("SMTP_SECURE", False)))
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
EMAIL_TIMEOUT = int(env("EMAIL_TIMEOUT", "5") or "5")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", env("CONTACT_FROM"))
SERVER_EMAIL = env("SERVER_EMAIL", DEFAULT_FROM_EMAIL)
CONTACT_TO = env_first("CONTACT_NOTIFICATION_RECIPIENT", "CONTACT_TO")
CONTACT_HMAC_SECRET = env("CONTACT_HMAC_SECRET")
TRUSTED_PROXY_IPS = set(env_list("TRUSTED_PROXY_IPS"))
AUDIT_INTERNAL_EMAIL = env("AUDIT_INTERNAL_EMAIL")
URGENCY_INTERNAL_EMAIL = env("URGENCY_INTERNAL_EMAIL")
INTERNAL_SMS_TO = env("INTERNAL_SMS_TO")
SMS_DRY_RUN = env_bool("SMS_DRY_RUN", True)
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = env("TWILIO_FROM_NUMBER")
WEBHOOK_URL = env_first("WEBHOOK_URL", "URGENCY_WEBHOOK_URL")
WEBHOOK_TOKEN = env_first("WEBHOOK_TOKEN", "URGENCY_WEBHOOK_TOKEN")

# Clé secrète HMAC pour la signature légale des réponses d'audit (AuditReponse.compute_signature)
AUDIT_SIGNATURE_KEY = env("AUDIT_SIGNATURE_KEY")

if not DEBUG:
    if not env("DATABASE_URL"):
        raise ImproperlyConfigured("DATABASE_URL must be set in production.")
    if len(CONTACT_HMAC_SECRET) < 32:
        raise ImproperlyConfigured("CONTACT_HMAC_SECRET must contain at least 32 characters in production.")
    if EMAIL_BACKEND != "django.core.mail.backends.smtp.EmailBackend":
        raise ImproperlyConfigured("The SMTP email backend is required in production.")
    if EMAIL_HOST.lower() != "smtp-relay.brevo.com":
        raise ImproperlyConfigured("EMAIL_HOST must use the approved Brevo SMTP relay in production.")
    if not all([EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL, SERVER_EMAIL]):
        raise ImproperlyConfigured(
            "EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL and SERVER_EMAIL are required in production."
        )
    if EMAIL_USE_TLS == EMAIL_USE_SSL:
        raise ImproperlyConfigured("Exactly one of EMAIL_USE_TLS or EMAIL_USE_SSL must be enabled in production.")
    if EMAIL_PORT <= 0 or EMAIL_TIMEOUT <= 0:
        raise ImproperlyConfigured("EMAIL_PORT and EMAIL_TIMEOUT must be positive in production.")
    for setting_name, address in (("DEFAULT_FROM_EMAIL", DEFAULT_FROM_EMAIL), ("SERVER_EMAIL", SERVER_EMAIL)):
        if "\r" in address or "\n" in address:
            raise ImproperlyConfigured(f"{setting_name} contains invalid header characters.")
        parsed_address = parseaddr(address)[1]
        try:
            validate_email(parsed_address)
        except Exception as exc:
            raise ImproperlyConfigured(f"{setting_name} must contain a valid email address.") from exc
        if parsed_address.rsplit("@", 1)[-1].lower() != "pixelprowlers.io":
            raise ImproperlyConfigured(f"{setting_name} must use the authenticated pixelprowlers.io domain.")


# ---------------------------------------------------------------------------
# Django Jazzmin — thème admin
# ---------------------------------------------------------------------------

JAZZMIN_SETTINGS = {
    "site_title": "PixelProwlers Admin",
    "site_header": "PixelProwlers · Administration",
    "site_brand": "PixelProwlers Cockpit",
    "site_logo": "cockpit/img/mark.svg",
    "login_logo": "cockpit/img/mark.svg",
    "site_logo_classes": "img-circle",
    "site_icon": "cockpit/img/mark.svg",
    "welcome_sign": "Bienvenue dans le cockpit PixelProwlers",
    "copyright": "PixelProwlers",

    # Modèles inclus dans la recherche rapide (barre en haut)
    # Ajuste les préfixes d'app selon l'emplacement réel de tes modèles
    "search_model": [],

    "user_avatar": None,

    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index"},
        {"name": "Voir le site", "url": "/", "new_window": True},
    ],

    # Ordre des apps dans la sidebar
    "order_with_respect_to": ["crm", "urgencies", "audits", "catalogue", "auth", "tracking"],
    "hide_models": [
        "crm.ContactDailyCounter",
        "audits.AuditDossierCounter",
        "audits.ClientDossierCounter",
        "audits.RdvRaison",
        "tracking.PageView",
        "tracking.QuestionInteraction",
    ],

    # Icônes FontAwesome par modèle
    # Format: "app_label.ModelName": "fa-solid fa-icone"
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        "crm.Contact": "fas fa-inbox",
        "crm.DiagnosticTicket": "fas fa-stethoscope",
        "urgencies.UrgencyRequest": "fas fa-triangle-exclamation",

        # ajuster selon l'app réelle si différente
        "urgencies.Rdv": "fas fa-calendar-check",
        "urgencies.RdvRappel": "fas fa-bell",
        "urgencies.RdvContact": "fas fa-address-book",
        "urgencies.CreneauCalendrier": "fas fa-calendar-alt",
        "urgencies.Motif": "fas fa-tags",
        "urgencies.RaisonAppel": "fas fa-phone",

        "audits.AuditDossier": "fas fa-folder-open",
        "audits.AuditDossierCounter": "fas fa-hashtag",
        "audits.AuditReponse": "fas fa-file-signature",
        "audits.RefonteAudit": "fas fa-tools",
        "audits.Citation": "fas fa-quote-right",

        "tracking": "fas fa-chart-line",
        "admin.LogEntry": "fas fa-clipboard-list",
        "catalogue": "fas fa-laptop",
        "catalogue.RefurbishedMachine": "fas fa-laptop-code",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # UX des formulaires
    "related_modal_active": True,
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,
    "custom_css": "cockpit/css/admin.css",

    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
