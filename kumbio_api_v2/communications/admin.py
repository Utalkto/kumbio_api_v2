# Django
from django.contrib import admin

# Models
from kumbio_api_v2.communications.models import MailTemplate, Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification model admin."""

    list_display = (
        "id",
        "created",
        "modified",
    )

    search_fields = (
        "title",
        "message",
    )

    list_filter = (
        "created",
        "modified",
    )

    readonly_fields = (
        "created",
        "modified",
    )


@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    """MailTemplate model admin."""

    list_display = (
        "id",
        "created",
        "modified",
    )

    search_fields = (
        "title",
        "message",
    )

    list_filter = (
        "created",
        "modified",
        "type",
    )

    readonly_fields = (
        "created",
        "modified",
    )
