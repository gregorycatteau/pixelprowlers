from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent


def load_env_file() -> None:
    import os

    env_path = PROJECT_DIR / ".env"
    if not env_path.exists():
        return

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
    import os

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


SECRET_KEY = env_first("DJANGO_SECRET_KEY", "SECRET_KEY", default="pixelprowlers-dev-insecure-change-me")
DEBUG = env_bool("DJANGO_DEBUG", env_bool("DEBUG", True))
ALLOWED_HOSTS = [
    host.strip()
    for host in env_first("DJANGO_ALLOWED_HOSTS", "ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "audits",
    "urgencies",
    "tracking",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("SMTP_HOST", "localhost")
EMAIL_PORT = int(env("SMTP_PORT", "25") or "25")
EMAIL_HOST_USER = env("SMTP_USER")
EMAIL_HOST_PASSWORD = env("SMTP_PASS")
EMAIL_USE_TLS = env_bool("SMTP_USE_TLS", env_bool("SMTP_SECURE", False))
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", env("CONTACT_FROM"))
CONTACT_TO = env("CONTACT_TO")
AUDIT_INTERNAL_EMAIL = env("AUDIT_INTERNAL_EMAIL")
URGENCY_INTERNAL_EMAIL = env("URGENCY_INTERNAL_EMAIL")
