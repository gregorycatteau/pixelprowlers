from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from .models import ClientDossier, ClientDossierCounter


def _month_key() -> str:
    return timezone.localdate().strftime("%y%m")


@transaction.atomic
def create_client_dossier(
    *,
    email: str = "",
    name: str = "",
    phone: str = "",
    source: str = "",
    phase: int = ClientDossier.Phase.CONTACT,
    metadata: dict | None = None,
) -> ClientDossier:
    month = _month_key()
    ClientDossierCounter.objects.bulk_create(
        [ClientDossierCounter(sequence_month=month, last_number=0)],
        ignore_conflicts=True,
    )
    counter = ClientDossierCounter.objects.select_for_update().get(sequence_month=month)
    counter.last_number += 1
    counter.save(update_fields=["last_number", "updated_at"])

    dossier = ClientDossier(
        sequence_month=month,
        sequence_number=counter.last_number,
        phase=phase,
        email=(email or "").strip().lower(),
        name=(name or "").strip(),
        phone=(phone or "").strip(),
        source=(source or "").strip(),
        metadata=metadata or {},
    )
    dossier.refresh_dossier_id()
    dossier.save()
    return dossier


@transaction.atomic
def get_or_create_client_dossier(
    *,
    email: str = "",
    name: str = "",
    phone: str = "",
    source: str = "",
    phase: int = ClientDossier.Phase.CONTACT,
    metadata: dict | None = None,
) -> tuple[ClientDossier, bool]:
    clean_email = (email or "").strip().lower()
    dossier = None

    if clean_email:
        dossier = (
            ClientDossier.objects.select_for_update()
            .filter(email__iexact=clean_email)
            .exclude(phase=ClientDossier.Phase.ARCHIVE)
            .order_by("-created_at")
            .first()
        )

    if dossier is None:
        return (
            create_client_dossier(
                email=clean_email,
                name=name,
                phone=phone,
                source=source,
                phase=phase,
                metadata=metadata,
            ),
            True,
        )

    changed_fields = []
    if name and not dossier.name:
        dossier.name = name.strip()
        changed_fields.append("name")
    if phone and not dossier.phone:
        dossier.phone = phone.strip()
        changed_fields.append("phone")
    if source and not dossier.source:
        dossier.source = source.strip()
        changed_fields.append("source")
    if metadata:
        dossier.metadata = {**(dossier.metadata or {}), **metadata}
        changed_fields.append("metadata")

    if changed_fields:
        changed_fields.append("updated_at")
        dossier.save(update_fields=changed_fields)

    if phase > dossier.phase:
        dossier.increment_phase(phase, reason=f"{source}: phase auto")

    return dossier, False


def attach_client_dossier(instance, *, phase: int = ClientDossier.Phase.CONTACT, source: str, metadata: dict | None = None):
    email = getattr(instance, "email", "") or getattr(getattr(instance, "contact", None), "email", "")
    phone = getattr(instance, "telephone", "") or getattr(instance, "phone", "") or getattr(getattr(instance, "contact", None), "telephone", "")
    first_name = getattr(instance, "prenom", "") or getattr(instance, "name", "") or getattr(getattr(instance, "contact", None), "prenom", "")
    last_name = getattr(instance, "nom", "") or getattr(getattr(instance, "contact", None), "nom", "")
    name = " ".join(part for part in [first_name, last_name] if part).strip()

    dossier, _created = get_or_create_client_dossier(
        email=email,
        name=name,
        phone=phone,
        source=source,
        phase=phase,
        metadata=metadata,
    )
    instance.client_dossier = dossier
    instance.save(update_fields=["client_dossier"])
    return dossier
