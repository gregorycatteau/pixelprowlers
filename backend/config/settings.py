import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def env_bool(name, default=False):
    """Convertit une variable d'environnement textuelle en booléen Django."""
    return os.getenv(name, str(default)).lower() in {'1', 'true', 'yes', 'on'}


def env_csv(name, default=''):
    """Transforme une liste séparée par des virgules en liste nettoyée."""
    return [
        item.strip()
        for item in os.getenv(name, default).split(',')
        if item.strip()
    ]


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', os.getenv('SECRET_KEY', 'dev-only-change-me'))
DEBUG = os.getenv('DJANGO_DEBUG', os.getenv('DEBUG', 'True')).lower() == 'true'

ALLOWED_HOSTS = env_csv('DJANGO_ALLOWED_HOSTS', os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1'))
CSRF_TRUSTED_ORIGINS = env_csv('DJANGO_CSRF_TRUSTED_ORIGINS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'pixelprowlers'),
        'USER': os.getenv('POSTGRES_USER', 'pixelprowlers'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', os.getenv('DB_PASSWORD', 'pixelprowlers')),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = env_csv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000')

SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', False)
SESSION_COOKIE_SECURE = env_bool('DJANGO_SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = env_bool('DJANGO_CSRF_COOKIE_SECURE', False)
SECURE_HSTS_SECONDS = int(os.getenv('DJANGO_SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
SECURE_HSTS_PRELOAD = env_bool('DJANGO_SECURE_HSTS_PRELOAD', False)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

CONTACT_TO = os.getenv('CONTACT_TO', '')
CONTACT_FROM = os.getenv('CONTACT_FROM', '')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('SMTP_HOST', '')
EMAIL_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_HOST_USER = os.getenv('SMTP_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASS', '')
EMAIL_USE_TLS = os.getenv('SMTP_SECURE', 'false').lower() != 'true'
EMAIL_USE_SSL = os.getenv('SMTP_SECURE', 'false').lower() == 'true'
