"""Organization sede serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import HeadquarterSchedule, Professional, Sede, Service


class OrganizationSedeSerializer(serializers.ModelSerializer):
    """Organization model serializer."""

    class Meta:
        """Meta class."""

        model = Sede
        fields = "__all__"


class ServiceSedeSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta class."""

        model = Service
        fields = "__all__"
        read_only_fields = ("sedes",)


class HeadquarterScheduleSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta class."""

        model = HeadquarterSchedule
        fields = "__all__"


class ServiceProfessionalSerializer(serializers.Serializer):
    """Proffesional schedule serializer."""

    service = serializers.DictField(required=True)

    def create(self, validated_data):
        sede = int(self.context.get("sede"))
        professional = self.context.get("professional")
        data_service = validated_data.get("service")
        # Create service
        service = Service.objects.create(**data_service)
        service.sedes.set([sede])
        # Create professional service
        professional_taken = Professional.objects.filter(pk=professional).last()
        if professional_taken:
            professional_taken.services.set([service])
        return service
