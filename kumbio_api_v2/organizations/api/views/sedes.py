"""Sedes views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from kumbio_api_v2.organizations.api.serializers import OrganizationSedeModelSerializer

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
    serializer_class = OrganizationSedeModelSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    queryset = Sede.objects.all().prefetch_related("sede_schedule")
