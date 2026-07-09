from django.contrib import admin
from django.conf import settings
from django.http import JsonResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql.validation.rules.custom.no_schema_introspection import NoSchemaIntrospectionCustomRule

from .schema import schema


def health_check(_request):
    return JsonResponse({"status": "ok"})


class SecureGraphQLView(GraphQLView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        if settings.DEBUG:
            kwargs.setdefault("graphiql", True)
        else:
            kwargs.setdefault("graphiql", False)
            kwargs.setdefault("validation_rules", [NoSchemaIntrospectionCustomRule])
        super().__init__(*args, **kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check),
    path("graphql/", SecureGraphQLView.as_view(schema=schema)),
]
