# Generated by Django 4.2.6 on 2023-10-10 23:09

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MembershipType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "membership_type",
                    models.CharField(
                        choices=[("FREE", "Gratis"), ("PRO", "Pro"), ("PREMIUM", "Premium")],
                        default="FREE",
                        max_length=10,
                    ),
                ),
                (
                    "appointments_allowed",
                    models.PositiveIntegerField(blank=True, null=True, verbose_name="Citas permitidas"),
                ),
                (
                    "places_allowed",
                    models.PositiveIntegerField(blank=True, null=True, verbose_name="Sedes permitidas"),
                ),
                (
                    "services_allowed",
                    models.PositiveIntegerField(blank=True, null=True, verbose_name="Servicios permitidos"),
                ),
                (
                    "professionals_allowed",
                    models.PositiveIntegerField(blank=True, null=True, verbose_name="Profesionales permitidos"),
                ),
                (
                    "email_notifications_allowed",
                    models.PositiveIntegerField(blank=True, null=True, verbose_name="Notificaciones permitidas"),
                ),
                (
                    "email_reminders_allowed",
                    models.PositiveIntegerField(blank=True, null=True, verbose_name="Recordatorios permitidos"),
                ),
                ("price", models.FloatField(blank=True, null=True, verbose_name="Pricio membresía")),
                ("trial_days", models.PositiveIntegerField(default=14)),
            ],
            options={
                "verbose_name": "Membresía",
                "verbose_name_plural": "Membresías",
            },
        ),
        migrations.CreateModel(
            name="Sector",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Date time on which the object was created.",
                        verbose_name="created at",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Date time on which the object was last modified.",
                        verbose_name="modified at",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("default_image", models.ImageField(blank=True, default=None, null=True, upload_to="organizations")),
            ],
            options={
                "verbose_name": "Sector",
                "verbose_name_plural": "Sectores",
            },
        ),
    ]
