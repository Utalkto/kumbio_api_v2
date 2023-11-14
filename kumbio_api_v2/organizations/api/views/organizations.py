"""Organization views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

# Serializers
from kumbio_api_v2.organizations.api.serializers import (
    OrganizationModelSerializer,
    OrganizationProfessionalModelSerializer,
    SectorModelSerializer,
)

# Models
from kumbio_api_v2.organizations.models import Organization, Professional, Sector


class OrganizationViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Organization view set.

    Handle sign up, login and account verification.
    """

    queryset = Organization.objects.filter()
    lookup_field = "pk"
    serializer_class = OrganizationModelSerializer
    permission_classes = [IsAuthenticated]


class OrganizationProfessionalsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List organization professionals."""

    serializer_class = OrganizationProfessionalModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_pk = self.kwargs["organization_pk"]
        return Professional.objects.filter(sede__organization_id=organization_pk)


class SectorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List sectors and subsectors."""

    queryset = Sector.objects.all()
    serializer_class = SectorModelSerializer
    permission_classes = [AllowAny]
