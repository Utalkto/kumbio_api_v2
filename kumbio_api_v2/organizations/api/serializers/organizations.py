"""Organizations serializers."""

# Utils
from datetime import datetime, timedelta

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
        fields = ["id", "name", "sub_sector", "description", "country", "currency", "how_you_know_us"]

    def create(self, data):
        # # Create organization
        request = self.context.get("request").query_params
        tutorial = request.get("tutorial")
        organization = Organization.objects.create(**data)
        # Create membreship
        membership = MembershipType.objects.get(membership_type="FREE_TRIAL")
        date_now = datetime.now().date()
        total_email_notifications = membership.email_notifications_allowed + membership.email_reminders_allowed
        total_wpp_notifications = membership.wpp_notifications_allowed + membership.wpp_reminders_allowed
        OrganizationMembership.objects.create(
            membership=membership,
            organization=organization,
            is_active=True,
            email_notification=membership.email,
            whatsapp_notification=membership.whatsapp,
            email_notification_available=total_email_notifications,
            wpp_notification_available=total_wpp_notifications,
            days_duration=membership.trial_days,
            start_date=date_now,
            expiration=date_now + timedelta(days=membership.trial_days),
        )
        if tutorial:
            # Create sede
            sede = Sede.objects.create(
                name=organization.name,
                organization=organization,
            )
            if sede:
                # Create professional
                request = self.context.get("request")
                user = request.user
                Professional.objects.create(user=user, sede=sede)
            # Create professional
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
