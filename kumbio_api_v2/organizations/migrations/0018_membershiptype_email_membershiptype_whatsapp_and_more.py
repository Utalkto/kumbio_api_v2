# Generated by Django 4.2.6 on 2023-11-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0017_remove_professional_is_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="membershiptype",
            name="email",
            field=models.BooleanField(
                default=False,
                help_text="Cuando esta en True significa que puede enviar notificaciones vía email.",
                verbose_name="Permite notificaciones por email",
            ),
        ),
        migrations.AddField(
            model_name="membershiptype",
            name="whatsapp",
            field=models.BooleanField(
                default=False,
                help_text="Cuando esta en True significa que puede enviar notificaciones vía wpp.",
                verbose_name="Permite notificaciones por wpp",
            ),
        ),
        migrations.AddField(
            model_name="membershiptype",
            name="wpp_notifications_allowed",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Notificaciones permitidas"),
        ),
        migrations.AddField(
            model_name="organizationmembership",
            name="email_notification",
            field=models.BooleanField(
                default=False,
                help_text="Cuando esta en True significa que puede enviar notificaciones vía email.",
                verbose_name="Notificaciones por email",
            ),
        ),
        migrations.AddField(
            model_name="organizationmembership",
            name="email_notification_available",
            field=models.PositiveIntegerField(default=0, verbose_name="Total notificaciones disponibles."),
        ),
        migrations.AddField(
            model_name="organizationmembership",
            name="whatsapp_notification",
            field=models.BooleanField(
                default=False,
                help_text="Cuando esta en True significa que puede enviar notificaciones vía wpp.",
                verbose_name="Notificaciones por wpp",
            ),
        ),
        migrations.AddField(
            model_name="organizationmembership",
            name="wpp_notification_available",
            field=models.PositiveIntegerField(default=0, verbose_name="Total notificaciones disponibles."),
        ),
        migrations.AlterField(
            model_name="membershiptype",
            name="membership_type",
            field=models.CharField(
                choices=[("FREE_TRIAL", "Free trial"), ("FREE", "Gratis"), ("PRO", "Pro"), ("PREMIUM", "Premium")],
                default="FREE",
                max_length=10,
            ),
        ),
    ]
