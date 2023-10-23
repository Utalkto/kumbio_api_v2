"""Sedes views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status

# Permissions
from rest_framework.permissions import (
    AllowAny,
)

# Models
from kumbio_api_v2.organizations.models import Sede

# Serializers
from kumbio_api_v2.organizations.api.serializers import (
    OrganizationSedeSerializer,
    ServiceSedeSerializer
)


class SedeViewset(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = OrganizationSedeSerializer
    lookup_field = 'pk'

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
        viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ServiceSedeSerializer
    lookup_field = 'pk'