"""Organizations serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import (
    MembershipType,
    Organization,
    OrganizationMembership,
    Professional,
    Sector,
    Sede,
    SubSector,
)


class OrganizationModelSerializer(serializers.ModelSerializer):
    """Organization model serializer."""

    description = serializers.CharField(required=False)

    class Meta:
        """Meta class."""

        model = Organization
        fields = ["name", "sub_sector", "description", "country", "currency", "how_you_know_us"]

    def create(self, data):
        # # Create organization
        request = self.context.get("request").query_params
        tutorial = request.get("tutorial")
        organization = Organization.objects.create(**data)
        # Create membreship
        OrganizationMembership.objects.create(
            membership=MembershipType.objects.get(membership_type="PREMIUM"),
            organization=organization,
            is_active=True,
        )
        if tutorial:
            # Create sede
            Sede.objects.create(
                name=organization.name,
                organization=organization,
            )
        return organization


class SubSectorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSector
        fields = ("name", "pk")


class SectorModelSerializer(serializers.ModelSerializer):
    sub_sectors = SubSectorModelSerializer(many=True, read_only=True)

    class Meta:
        model = Sector
        fields = ("name", "sub_sectors")


class OrganizationProfessionalModelSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = Professional
        fields = ["full_name", "pk"]
