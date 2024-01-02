# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import Professional, Service


class ProfessioanlServicesModelSerializer(serializers.ModelSerializer):
    """Rest professional model serializer."""

    class Meta:
        """Meta class."""

        model = Service
        fields = ["name", "price", "duration"]


class OrganizationProfessionalModelSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = Professional
        exclude = ["services"]


class ServicesOrganizationModelSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    professionals = OrganizationProfessionalModelSerializer(source="service_professionals", many=True, read_only=True)
    service_professionals = serializers.ListField(child=serializers.IntegerField(required=False), write_only=True)

    class Meta:
        """Meta class."""

        model = Service
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        professionals = validated_data.pop("service_professionals")
        obj = super().create(validated_data)
        if professionals:
            professionals = Professional.objects.filter(id__in=professionals)
            for professional in professionals:
                professional.services.add(obj)
        return obj
