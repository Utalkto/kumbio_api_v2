"""Organization views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import (
    AllowAny,
)

# Serializers
from kumbio_api_v2.organizations.api.serializers import (
    OrganizationModelSerializer
)

# Models
from kumbio_api_v2.organizations.models import Organization


class OrganizationViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    """Organization view set.

    Handle sign up, login and account verification.
    """

    queryset = Organization.objects.filter()
    lookup_field = 'pk'
    serializer_class = OrganizationModelSerializer
    permission_classes = [AllowAny]
