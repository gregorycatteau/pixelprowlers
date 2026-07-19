from django.conf import settings
from django.core.cache import cache
from graphql import GraphQLError


CAPABILITY_LOOKUP_LIMIT = 30
CAPABILITY_LOOKUP_WINDOW_SECONDS = 15 * 60


def _request_from_info(info):
    context = getattr(info, "context", None)
    return getattr(context, "request", context)


def _client_ip(request) -> str:
    if request is None:
        return "unknown"

    remote_addr = request.META.get("REMOTE_ADDR", "unknown")
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded and remote_addr in getattr(settings, "TRUSTED_PROXY_IPS", set()):
        return forwarded.rsplit(",", 1)[-1].strip()
    return remote_addr


def enforce_capability_rate_limit(info, scope: str) -> None:
    request = _request_from_info(info)
    key = f"graphql-capability:{scope}:{_client_ip(request)}"
    if cache.add(key, 1, timeout=CAPABILITY_LOOKUP_WINDOW_SECONDS):
        return

    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=CAPABILITY_LOOKUP_WINDOW_SECONDS)
        return

    if count > CAPABILITY_LOOKUP_LIMIT:
        raise GraphQLError("Ressource indisponible.")
