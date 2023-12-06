# Django
from django.contrib import admin

# Models
from kumbio_api_v2.communications.models import MailTemplate, Notification, QueueMessage


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification model admin."""

    list_display = (
        "id",
        "organization",
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
        "name",
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


@admin.register(QueueMessage)
class QueueMessageAdmin(admin.ModelAdmin):
    """QueueMessage model admin."""

    list_display = ["user", "message_type", "sent", "attempts", "issue_sent", "phone_number"]
