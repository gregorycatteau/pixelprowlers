from graphene_django import DjangoObjectType

from .models import UrgencyRequest


class UrgencyRequestType(DjangoObjectType):
    class Meta:
        model = UrgencyRequest
        fields = ("reference", "status")
