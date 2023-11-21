# Django
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

User = get_user_model()


# Models
from kumbio_api_v2.users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = [
        [
            ("Datos de usuario"),
            {
                "fields": ("first_name", "last_name", "password"),
            },
        ],
        [
            ("Datos de contacto"),
            {
                "fields": ("email", "username", "phone_number"),
            },
        ],
        [
            ("Tipo usuario"),
            {
                "fields": ("is_client", "is_owner", "is_professional", "is_staff"),
            },
        ],
        [
            ("Stats"),
            {
                "fields": ("last_login", "date_joined"),
            },
        ],
    ]
    list_display = ["email", "first_name", "is_owner", "is_client", "is_professional"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    inlines = [ProfileInline]
