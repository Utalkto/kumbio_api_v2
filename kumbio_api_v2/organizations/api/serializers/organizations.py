"""Organizations serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import Organization


class OrganizationModelSerializer(serializers.ModelSerializer):
    """Organization model serializer."""

    class Meta:
        """Meta class."""

        model = Organization
        fields = (
            "name",
            "description",
        )
