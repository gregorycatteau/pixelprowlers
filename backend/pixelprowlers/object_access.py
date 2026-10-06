"""Object authority using existing Django sessions and signing, never public IDs."""
import re
import time
from urllib.parse import urlsplit
from django.conf import settings
from django.core import signing
from graphql import GraphQLError

DENIED = "Accès au dossier non autorisé."
MAX_AGE = 30 * 24 * 3600

def request_from_info(info):
    context = getattr(info, "context", None)
    return getattr(context, "request", context)

def require_same_origin(request):
    origin = request.headers.get("Origin", "") if request else ""
    # Browser mutations send Origin; non-browser callers also require an allowed Origin.
    allowed = set(getattr(settings, "CORS_ALLOWED_ORIGINS", []))
    if request:
        allowed.add(f"{request.scheme}://{request.get_host()}")
    if not origin or origin not in allowed:
        raise GraphQLError(DENIED)

def grant_object(request, kind, reference, pk):
    require_same_origin(request)
    if not hasattr(request, "session"):
        raise GraphQLError(DENIED)
    owner = request.user.pk if request.user.is_authenticated else None
    claims = request.session.get("public_object_grants", [])
    claims = [c for c in claims if c["expires"] > time.time() and c["owner"] == owner][-19:]
    claims.append({"kind": kind, "reference": reference, "pk": pk,
                   "owner": owner, "expires": time.time() + MAX_AGE})
    request.session["public_object_grants"] = claims

def owned_object(request, kind, reference, model):
    require_same_origin(request)
    owner = request.user.pk if request.user.is_authenticated else None
    for claim in request.session.get("public_object_grants", []):
        if (claim["kind"] == kind and claim["reference"] == reference
                and claim["owner"] == owner and claim["expires"] > time.time()):
            obj = model.objects.filter(pk=claim["pk"]).first()
            if obj is not None:
                return obj
    raise GraphQLError(DENIED)

def diagnostic_capability(ticket):
    return signing.dumps({"pk": ticket.pk}, salt="pixelprowlers.diagnostic.followup.v1")

def diagnostic_object(capability, model):
    try:
        payload = signing.loads(capability, salt="pixelprowlers.diagnostic.followup.v1", max_age=MAX_AGE)
        obj = model.objects.filter(pk=payload["pk"]).first()
        if obj is not None:
            return obj
    except (signing.BadSignature, KeyError, TypeError, ValueError):
        pass
    raise GraphQLError(DENIED)

def contact_object(token, model):
    if not re.fullmatch(r"[A-Za-z0-9_-]{43}", token):
        raise GraphQLError(DENIED)
    obj = model.objects.filter(secret_token=token).first()
    if obj is None:
        raise GraphQLError(DENIED)
    return obj

def public_site_url():
    # Never derive capability-bearing links from a browser-controlled Origin.
    url = getattr(settings, "PUBLIC_SITE_URL", "https://pixelprowlers.io").rstrip("/")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc not in {"pixelprowlers.io", "www.pixelprowlers.io"} or parsed.path:
        return "https://pixelprowlers.io"
    return url
