# Django
from django.contrib import admin

# Models
from kumbio_api_v2.organizations.models import MembershipType, Organization, OrganizationMembership, Sector


class OrganizationMembershipInline(admin.TabularInline):
    model = OrganizationMembership
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["name", "sector", "country"]
    search_fields = ["name"]
    list_filter = ["sector", "country"]
    inlines = [OrganizationMembershipInline]


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["membership", "organization"]
    search_fields = ["organization__name"]
    list_filter = ["organization__name"]


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["membership_type"]
    search_fields = ["membership_type"]
    list_filter = ["membership_type"]
