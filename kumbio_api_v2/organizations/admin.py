# Django
from django.contrib import admin

# Models
from kumbio_api_v2.organizations.models import (
    MembershipType,
    Organization,
    OrganizationMembership,
    Professional,
    Sector,
    Sede,
    Service,
)


class OrganizationMembershipInline(admin.StackedInline):
    model = OrganizationMembership
    extra = 0


class OrganizationSedeInline(admin.TabularInline):
    model = Sede
    extra = 0


class SedeServicesInline(admin.TabularInline):
    model = Service.sedes.through
    extra = 0


class SedeProfesionalInline(admin.TabularInline):
    model = Professional
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["name", "sector", "country"]
    search_fields = ["name"]
    list_filter = ["sector", "country"]
    inlines = [OrganizationSedeInline, OrganizationMembershipInline]


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["membership_type"]
    search_fields = ["membership_type"]
    list_filter = ["membership_type"]


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    """Sede model admin."""

    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]
    inlines = [SedeProfesionalInline, SedeServicesInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Service sede model admin."""

    list_display = ["name", "duration", "price"]
    search_fields = ["name"]
    list_filter = ["name"]
    autocomplete_fields = ["sedes"]


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    """Service sede model admin."""

    autocomplete_fields = ["services"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "servicios":
            if "sede" in request.GET:
                sede_id = request.GET["sede"]
                sede = Sede.objects.get(id=sede_id)
                kwargs["queryset"] = sede.servicios.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
