"""Countries views."""
# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import AllowAny

# Serializers
from kumbio_api_v2.organizations.api.serializers import CountryModelSerializer

# Models
from kumbio_api_v2.organizations.models import Country


class CountryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List countries."""

    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    permission_classes = [AllowAny]
