# Existing locally installed Python 3.13 historical runtime; no dependency installation.
ARG BASE_IMAGE=pixelprowlers-django:security-base-efd98e84bc44
FROM ${BASE_IMAGE}
ARG DELIVERY_SHA
WORKDIR /srv/pixelprowlers-backend
COPY . .
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN DJANGO_DEBUG=True DJANGO_SECRET_KEY=build-only-not-production POSTGRES_PASSWORD=build-only-not-production python manage.py collectstatic --noinput
LABEL org.opencontainers.image.revision=${DELIVERY_SHA} pixelprowlers.source.base=09b2cde900083bf7f0160292fbccc5225118d0ae
# Explicitly no automatic migrate: this correction has no model/schema changes.
CMD ["gunicorn", "pixelprowlers.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
