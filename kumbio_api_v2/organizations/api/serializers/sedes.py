"""Organization sede serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import (
    Professional,
    Sede,
    Service,
    ProfessionalSchedule,
    HeadquarterSchedule
)
from kumbio_api_v2.users.models import User


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


class ProfessionalScheduleModelSerializer(serializers.ModelSerializer):
    """Service model serializer."""

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


class ProfessionalScheduleSerializer(serializers.Serializer):
    """Proffesional schedule serializer."""

    professional_schedule = serializers.ListField(
        child=serializers.DictField(required=True)
    )

    def create(self, validated_data):
        sede = self.context.get("sede")
        professional = self.context.get("professional")
        tutorial = self.context.get("tutorial")
        professional_schedule = validated_data.get("professional_schedule")
        for schedule in professional_schedule:
            schedule["professional"] = professional
            serializer_professional = ProfessionalScheduleModelSerializer(data=schedule)
            serializer_professional.is_valid(raise_exception=True)
            serializer_professional.save()
            if tutorial:
                schedule.pop("professional")
                schedule["sede"] = sede
                serializer_headquarter =HeadquarterScheduleSerializer(data=schedule)
                serializer_headquarter.is_valid(raise_exception=True)
                serializer_headquarter.save()
        professional
        return professional