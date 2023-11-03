# Django
from django.contrib import admin

# Models
from kumbio_api_v2.organizations.models import (
    Country,
    HeadquarterSchedule,
    MembershipType,
    Organization,
    OrganizationMembership,
    Professional,
    ProfessionalSchedule,
    Sector,
    Sede,
    Service,
    SubSector,
    RestProfessionalSchedule
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


class SubSectorInline(admin.TabularInline):
    model = SubSector
    extra = 0


class HeadquarterScheduleInline(admin.TabularInline):
    model = HeadquarterSchedule
    extra = 0


class ProfessionalScheduleInline(admin.TabularInline):
    model = ProfessionalSchedule
    extra = 0


class RestProfessionalScheduleInline(admin.TabularInline):
    model = RestProfessionalSchedule
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["name", "sub_sector", "country"]
    search_fields = ["name"]
    list_filter = ["sub_sector", "country", "how_you_know_us"]
    inlines = [OrganizationSedeInline, OrganizationMembershipInline]


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]
    inlines = [SubSectorInline]


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
    inlines = [HeadquarterScheduleInline, SedeProfesionalInline, SedeServicesInline]


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

    list_display = ["user", "sede"]
    autocomplete_fields = ["services"]
    inlines = [ProfessionalScheduleInline, RestProfessionalScheduleInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "servicios":
            if "sede" in request.GET:
                sede_id = request.GET["sede"]
                sede = Sede.objects.get(id=sede_id)
                kwargs["queryset"] = sede.servicios.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Service sede model admin."""

    list_display = ["name", "slug_name", "phone_prefix"]
    search_fields = ["name", "phone_prefix"]
    list_filter = ["name", "phone_prefix"]


# @admin.register(RestProfessionalSchedule)
# class RestProfessionalScheduleAdmin(admin.ModelAdmin):
#     """Service sede model admin."""

#     list_display = ["professional"]
