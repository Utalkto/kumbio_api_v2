"""Sedes views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from kumbio_api_v2.organizations.api.serializers import (
    OrganizationSedeSerializer,
    ProfessionalSerializer,
    ServiceSedeSerializer,
)

# Models
from kumbio_api_v2.organizations.models import Sede


class SedeViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrganizationSedeSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        queryset = Sede.objects.filter(organization__pk=organization_pk)
        return queryset


class ServiceSedeViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ServiceSedeSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]


class ProfesionalViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ProfessionalSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
