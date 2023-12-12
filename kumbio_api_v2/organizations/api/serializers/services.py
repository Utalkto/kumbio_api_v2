# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import Service


class ProfessioanlServicesModelSerializer(serializers.ModelSerializer):
    """Rest professional model serializer."""

    class Meta:
        """Meta class."""

        model = Service
        fields = ["name", "price", "duration"]


class ServicesOrganizationModelSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta class."""

        model = Service
        fields = "__all__"
