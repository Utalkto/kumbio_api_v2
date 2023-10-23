"""Organization sede serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import Sede, Service


class OrganizationSedeSerializer(serializers.ModelSerializer):
    """Organization model serializer."""

    class Meta:
        """Meta class."""

        model = Sede
        fields = '__all__'

    
class ServiceSedeSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta class."""

        model = Service
        fields = '__all__'
        read_only_fields = ('sedes',)