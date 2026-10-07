from django.contrib import admin
from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404
from django.urls import path
from pathlib import Path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql import specified_rules
from graphql.validation.rules.custom.no_schema_introspection import NoSchemaIntrospectionCustomRule

from .schema import schema


def health_check(_request):
    return JsonResponse({"status": "ok"})


def collected_static(_request, asset):
    root = Path(settings.STATIC_ROOT).resolve()
    target = (root / asset).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise Http404
    response = FileResponse(target.open("rb"))
    response["Cache-Control"] = "public, max-age=3600"
    response["X-Content-Type-Options"] = "nosniff"
    return response


class SecureGraphQLView(GraphQLView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response["Cache-Control"] = "no-store"
        response["Referrer-Policy"] = "no-referrer"
        return response

    def __init__(self, *args, **kwargs):
        if settings.DEBUG:
            kwargs.setdefault("graphiql", True)
        else:
            kwargs.setdefault("graphiql", False)
            kwargs.setdefault("validation_rules", [*specified_rules, NoSchemaIntrospectionCustomRule])
        super().__init__(*args, **kwargs)


urlpatterns = [
    path("static/<path:asset>", collected_static),
    path("admin/", admin.site.urls),
    path("health/", health_check),
    path("graphql/", SecureGraphQLView.as_view(schema=schema)),
]
