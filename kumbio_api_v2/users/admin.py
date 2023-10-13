# Django
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

User = get_user_model()


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
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ],
        [
            ("Stats"),
            {
                "fields": ("last_login", "date_joined"),
            },
        ],
    ]
    list_display = ["email", "name", "is_superuser"]
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
