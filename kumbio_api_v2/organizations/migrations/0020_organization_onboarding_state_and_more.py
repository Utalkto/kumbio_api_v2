# Generated by Django 4.2.6 on 2023-12-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0019_membershiptype_wpp_reminders_allowed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="onboarding_state",
            field=models.CharField(
                blank=True,
                default="organization_created",
                max_length=120,
                null=True,
                verbose_name="Estado de onboarding",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="how_you_know_us",
            field=models.CharField(
                blank=True, default=None, max_length=60, null=True, verbose_name="Como nos conocio"
            ),
        ),
    ]