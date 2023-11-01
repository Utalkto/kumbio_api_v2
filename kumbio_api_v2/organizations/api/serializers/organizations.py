"""Organizations serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import Organization, Sector, SubSector


class OrganizationModelSerializer(serializers.ModelSerializer):
    """Organization model serializer."""

    class Meta:
        """Meta class."""

        model = Organization
        fields = (
            "name",
            "description",
        )


class SubSectorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSector
        fields = ("name", "pk")


class SectorModelSerializer(serializers.ModelSerializer):
    sub_sectors = SubSectorModelSerializer(many=True, read_only=True)

    class Meta:
        model = Sector
        fields = ("name", "sub_sectors")
