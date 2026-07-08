import os
from pathlib import Path
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent
DEV_INSECURE_SECRET_KEY = "pixelprowlers-dev-insecure-change-me"


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


SECRET_KEY = env_first("DJANGO_SECRET_KEY", "SECRET_KEY", default=DEV_INSECURE_SECRET_KEY)
DEBUG = env_bool("DJANGO_DEBUG", env_bool("DEBUG", True))

if not DEBUG and (not SECRET_KEY or SECRET_KEY == DEV_INSECURE_SECRET_KEY):
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production.")

ALLOWED_HOSTS = [
    host.strip()
    for host in env_first("DJANGO_ALLOWED_HOSTS", "ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
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
    "crm",
    "urgencies",
    "tracking",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
    default="http://localhost:3000,http://localhost:5173,https://pixelprowlers.io,https://www.pixelprowlers.io",
)
CORS_ALLOW_CREDENTIALS = env_bool("CORS_ALLOW_CREDENTIALS", False)

CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default="http://localhost:3000,http://localhost:5173,https://pixelprowlers.io,https://www.pixelprowlers.io",
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = env_bool("DJANGO_USE_X_FORWARDED_HOST", True)
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not DEBUG)
SECURE_HSTS_SECONDS = int(env("DJANGO_SECURE_HSTS_SECONDS", "0") or "0")
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend" if env("SMTP_HOST") else "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = env("SMTP_HOST", "localhost")
EMAIL_PORT = int(env("SMTP_PORT", "25") or "25")
EMAIL_HOST_USER = env("SMTP_USER")
EMAIL_HOST_PASSWORD = env("SMTP_PASS")
EMAIL_USE_TLS = env_bool("SMTP_USE_TLS", env_bool("SMTP_SECURE", False))
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", env("CONTACT_FROM"))
CONTACT_TO = env("CONTACT_TO")
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


# ---------------------------------------------------------------------------
# Django Jazzmin — thème admin
# ---------------------------------------------------------------------------

JAZZMIN_SETTINGS = {
    "site_title": "PixelProwlers Admin",
    "site_header": "PixelProwlers",
    "site_brand": "PixelProwlers",
    "site_logo": None,
    "login_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Bienvenue dans le cockpit PixelProwlers",
    "copyright": "PixelProwlers",

    # Modèles inclus dans la recherche rapide (barre en haut)
    # Ajuste les préfixes d'app selon l'emplacement réel de tes modèles
    "search_model": [
        "urgencies.Rdv",
        "audits.AuditDossier",
    ],

    "user_avatar": None,

    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index"},
        {"name": "Voir le site", "url": "/", "new_window": True},
    ],

    # Ordre des apps dans la sidebar
    "order_with_respect_to": ["auth", "audits", "urgencies", "tracking"],

    # Icônes FontAwesome par modèle
    # Format: "app_label.ModelName": "fa-solid fa-icone"
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

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
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # UX des formulaires
    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,

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
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
