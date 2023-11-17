"""Countries views."""
# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Models
from kumbio_api_v2.organizations.models import Country

# Serializers
from kumbio_api_v2.organizations.api.serializers import CountryModelSerializer


class CountryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List countries."""

    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    permission_classes = [AllowAny]
