"""Professionals serializers."""

# Django


# Django REST Framework
from rest_framework import serializers

# Serializers
from kumbio_api_v2.organizations.api.serializers.sedes import HeadquarterScheduleSerializer
from kumbio_api_v2.organizations.api.serializers.services import ProfessioanlServicesModelSerializer

# Models
from kumbio_api_v2.organizations.models import Professional, ProfessionalSchedule, RestProfessionalSchedule, Sede
from kumbio_api_v2.users.api.serializers.users import UserModelSerializer
from kumbio_api_v2.users.models import User


class RestProfessionalScheduleModelSerializer(serializers.ModelSerializer):
    """Rest professional model serializer."""

    date_init = serializers.DateField()

    class Meta:
        """Meta class."""

        model = RestProfessionalSchedule
        fields = ["professional", "date_init", "date_end", "description"]

    def validate_date_init(self, value):
        professional = self.context.get("professional")
        taken_rest = RestProfessionalSchedule.objects.filter(professional=professional, date_init=value).exists()
        if taken_rest:
            raise serializers.ValidationError("Ya existe un tiempo libre con esta fecha.")
        return value


class ProfessionalScheduleModelSerializer(serializers.ModelSerializer):
    """Rest professional model serializer."""

    class Meta:
        """Meta class."""

        model = ProfessionalSchedule
        fields = ["day", "hour_init", "hour_end", "hour_init_rest", "hour_end_rest"]


class ProfessionalModelSerializer(serializers.ModelSerializer):
    """Professional model serializer."""

    user = UserModelSerializer()
    professional_schedule = serializers.SerializerMethodField()
    professional_services = serializers.SerializerMethodField()

    def get_professional_schedule(self, obj):
        schedule = obj.professional_schedule.all()
        professional_schedule = []
        for item in schedule:
            serializer = ProfessionalScheduleModelSerializer(item)
            professional_schedule.append(serializer.data)
        return professional_schedule

    def get_professional_services(self, obj):
        services = obj.services.all()
        professional_services = []
        if services:
            for item in services:
                serializer = ProfessioanlServicesModelSerializer(item)
                professional_services.append(serializer.data)
        return professional_services

    class Meta:
        """Meta class."""

        model = Professional
        fields = ["user", "sede", "description", "professional_schedule", "professional_services"]


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
        tutorial = self.context.get("tutorial")
        professional_schedule = validated_data.get("professional_schedule")
        sede_pk = validated_data.get("sede_pk")
        if tutorial:
            request = self.context.get("request")
            user = request.user
            sede = Sede.objects.filter(id=sede_pk).first()
            professional, _ = Professional.objects.update_or_create(
                user=user,
                defaults={
                    "sede": sede,
                },
            )
            validated_data["professional_pk"] = professional.pk
        else:
            professional = self.context.get("professional")
        # Delete current schedule
        professional.professional_schedule.all().delete()
        for schedule in professional_schedule:
            day = schedule.get("day")
            hour_init = schedule.get("hour_init")
            hour_end = schedule.get("hour_end")
            hour_init_rest = schedule.get("hour_init_rest")
            hour_end_rest = schedule.get("hour_end_rest")
            professional.professional_schedule.create(
                day=day,
                hour_init=hour_init,
                hour_end=hour_end,
                hour_init_rest=hour_init_rest,
                hour_end_rest=hour_end_rest,
            )
            if tutorial:
                schedule["sede"] = sede_pk
                serializer_headquarter = HeadquarterScheduleSerializer(data=schedule)
                serializer_headquarter.is_valid(raise_exception=True)
                serializer_headquarter.save()
        return validated_data
