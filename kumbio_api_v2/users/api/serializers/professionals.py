"""Professionals serializers."""

# Django


# Django REST Framework
from rest_framework import serializers

# Serializers
from kumbio_api_v2.organizations.api.serializers.sedes import HeadquarterScheduleSerializer

# Models
from kumbio_api_v2.organizations.models import Professional, RestProfessionalSchedule, Sede
from kumbio_api_v2.users.api.serializers.users import UserModelSerializer
from kumbio_api_v2.users.models import User


class RestProfessionalScheduleModelSerializer(serializers.ModelSerializer):
    """Rest professional model serializer."""

    class Meta:
        """Meta class."""

        model = RestProfessionalSchedule
        fields = "__all__"


class ProfessionalModelSerializer(serializers.ModelSerializer):
    """Professional model serializer."""

    user = UserModelSerializer()
    
    class Meta:
        """Meta class."""

        model = Professional
        fields = ["user", "sede", "description"]


class ProfessionalSerializer(serializers.Serializer):
    """Professional model serializer."""

    user_data = UserModelSerializer()
    sede_pk = serializers.IntegerField(required=False)
    service_pk = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    how_you_know_us = serializers.CharField(required=False)

    def create(self, validated_data):
        request = self.context.get("request")
        tutorial = self.context.get("tutorial")
        user_data = validated_data.get("user_data")
        user_data["is_professional"] = True
        sede_pk = validated_data.get("sede_pk")
        # Create user
        if tutorial:
            user = request.user
            user.first_name = user_data.get("first_name")
            user.last_name = user_data.get("last_name")
            user.phone_number = user_data.get("phone_number")
            user.is_professional = user_data.get("is_professional")
            user.save()
        else:
            user = User.objects.create_user(**user_data)
        if sede_pk and user:
            sede = Sede.objects.get(id=sede_pk)
            professional = Professional.objects.create(user=user, sede=sede, is_user=True)
            organization = professional.organization
            how_you_know_us = validated_data.get("how_you_know_us")
            organization.how_you_know_us = how_you_know_us
            organization.save()
        return validated_data


class ProfessionalScheduleSerializer(serializers.Serializer):
    """Proffesional schedule serializer."""

    professional_schedule = serializers.ListField(child=serializers.DictField(required=True))
    sede_pk = serializers.IntegerField(required=False)

    def create(self, validated_data):
        professional = self.context.get("professional")
        rest_professional = self.context.get("rest")
        tutorial = self.context.get("tutorial")
        professional_schedule = validated_data.get("professional_schedule")
        sede_pk = validated_data.get("sede_pk")
        # Delete current schedule
        if rest_professional:
            professional.rest_professional_schedule.all().delete()
            for schedule in professional_schedule:
                day = schedule.get("day")
                hour_init = schedule.get("hour_init")
                hour_end = schedule.get("hour_end")
                professional.rest_professional_schedule.create(
                    day=day,
                    hour_init=hour_init,
                    hour_end=hour_end,
                )
        else:
            professional.professional_schedule.all().delete()
            for schedule in professional_schedule:
                day = schedule.get("day")
                hour_init = schedule.get("hour_init")
                hour_end = schedule.get("hour_end")
                professional.professional_schedule.create(
                    day=day,
                    hour_init=hour_init,
                    hour_end=hour_end,
                )
                if tutorial:
                    schedule.pop("professional")
                    schedule["sede"] = sede_pk
                    serializer_headquarter = HeadquarterScheduleSerializer(data=schedule)
                    serializer_headquarter.is_valid(raise_exception=True)
                    serializer_headquarter.save()
        return validated_data
