# Generated by Django 4.2.6 on 2023-11-30 21:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0018_membershiptype_email_membershiptype_whatsapp_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="membershiptype",
            name="wpp_reminders_allowed",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Recordatorios wpp permitidos"),
        ),
        migrations.AlterField(
            model_name="membershiptype",
            name="email_notifications_allowed",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Notificaciones email permitidas"),
        ),
        migrations.AlterField(
            model_name="membershiptype",
            name="email_reminders_allowed",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Recordatorios email permitidos"),
        ),
        migrations.AlterField(
            model_name="membershiptype",
            name="wpp_notifications_allowed",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Notificaciones por wpp permitidas"),
        ),
        migrations.AlterField(
            model_name="organizationmembership",
            name="email_notification_available",
            field=models.PositiveIntegerField(default=0, verbose_name="Total notificaciones vía email disponibles."),
        ),
        migrations.AlterField(
            model_name="organizationmembership",
            name="wpp_notification_available",
            field=models.PositiveIntegerField(default=0, verbose_name="Total notificaciones vía wpp disponibles."),
        ),
    ]
