"""Organization sede serializers."""


# Django REST Framework
from rest_framework import serializers

from kumbio_api_v2.organizations.api.serializers.services import OrganizationProfessionalModelSerializer

# Models
from kumbio_api_v2.organizations.models import HeadquarterSchedule, Professional, ProfessionalSchedule, Sede, Service

# Serializers
from kumbio_api_v2.users.api.serializers.users import UserModelSerializer
from kumbio_api_v2.users.models import User


class HeadquarterScheduleSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta class."""

        model = HeadquarterSchedule
        fields = "__all__"


class ServiceSedeSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta class."""

        model = Service
        fields = "__all__"
        read_only_fields = ("sedes",)


class OrganizationSedeModelSerializer(serializers.ModelSerializer):
    """Organization model serializer."""

    sede_schedule = HeadquarterScheduleSerializer(many=True, read_only=True)
    sede_services = ServiceSedeSerializer(many=True, read_only=True)
    sede_professionals = OrganizationProfessionalModelSerializer(source="organization_professionals", many=True, read_only=True)
    create_sede_schedule = serializers.ListField(child=serializers.DictField(), write_only=True)
    create_sede_services = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    create_sede_professionals = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        """Meta class."""

        model = Sede
        fields = [
            "id",
            "name",
            "description",
            "sede_type",
            "address",
            "maps_url",
            "phone",
            "phone_aux",
            "organization",
            "sede_professionals",
            "sede_services",
            "sede_schedule",
            "create_sede_schedule",
            "create_sede_services",
            "create_sede_professionals",
        ]

    def create(self, validated_data):
        sede_schedule = validated_data.pop("create_sede_schedule")
        sede_services = validated_data.pop("create_sede_services")
        sede_professionals = validated_data.pop("create_sede_professionals")
        sede = Sede.objects.create(**validated_data)
        for schedule in sede_schedule:
            schedule["sede"] = sede.pk
        sede_schedule = HeadquarterScheduleSerializer(data=sede_schedule, many=True)
        try:
            sede_schedule.is_valid(raise_exception=True)
        except Exception as e:
            sede.delete()
            raise e
        sede_schedule.save()
        sede_services = Service.objects.filter(pk__in=sede_services)
        for service in sede_services.iterator():
            service.sedes.add(sede)
        sede_professionals = Professional.objects.filter(pk__in=sede_professionals)
        for professional in sede_professionals.iterator():
            professional.sede = sede
            professional.save(update_fields=["sede"])
        return sede


class ProfessionalScheduleModelSerializer(serializers.ModelSerializer):
    """Professional model serializer."""

    class Meta:
        """Meta class."""

        model = ProfessionalSchedule
        fields = "__all__"


class ProfessionalSerializer(serializers.Serializer):
    """Professional model serializer."""

    first_name = serializers.CharField(min_length=2, max_length=255)
    last_name = serializers.CharField(min_length=2, max_length=255)
    phone_number = serializers.CharField(max_length=255)
    sede_pk = serializers.IntegerField()

    def create(self, data):
        request = self.context.get("request")
        tutorial = self.context.get("tutorial")
        sede = self.context.get("sede")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        sede_pk = data.get("sede_pk")
        if tutorial:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.is_professional = True
            user.save()
        else:
            user, _ = User.objects.update_or_create(
                phone_number=phone_number,
                defaults={"first_name": first_name, "last_name": last_name, "is_professional": True},
            )
        sede = Sede.objects.get(id=sede_pk)
        Professional.objects.update_or_create(user=user, defaults={"sede": sede, "is_user": True})
        return data


class ServiceProfessionalSerializer(serializers.Serializer):
    """Proffesional schedule serializer."""

    service = serializers.DictField(required=True)
    sede_pk = serializers.IntegerField(required=False)

    def create(self, validated_data):
        sede_pk = validated_data.get("sede_pk")
        data_service = validated_data.get("service")
        professional = self.context.get("professional")
        # Create service
        service = Service.objects.create(**data_service)
        service.sedes.set([sede_pk])
        # Add professional service
        professional.services.add(service)
        return validated_data


class SedeProfessionalModelSerializer(serializers.ModelSerializer):
    """Proffesional schedule serializer."""

    user = UserModelSerializer()

    class Meta:
        """Meta class."""

        model = Professional
        fields = ["id", "user"]
