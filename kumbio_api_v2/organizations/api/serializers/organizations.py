"""Organizations serializers."""

# Utils
from datetime import datetime, timedelta

# Django REST Framework
from rest_framework import serializers

from kumbio_api_v2.organizations.api.serializers.sedes import OrganizationSedeModelSerializer
from kumbio_api_v2.organizations.models import (
    MembershipType,
    Organization,
    OrganizationMembership,
    Professional,
    Sector,
    Sede,
    SubSector,
)

# Models
from kumbio_api_v2.users.models import Profile


class OrganizationModelSerializer(serializers.ModelSerializer):
    """Organization model serializer."""

    description = serializers.CharField(required=False)
    organization_sedes = OrganizationSedeModelSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Organization
        fields = "__all__"

    def create(self, data):
        # # Create organization
        request = self.context.get("request")
        params = request.query_params
        user = request.user
        tutorial = params.get("tutorial")
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
            # Create profile
            Profile.objects.create(
                user=user,
                organization=organization,
            )
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
