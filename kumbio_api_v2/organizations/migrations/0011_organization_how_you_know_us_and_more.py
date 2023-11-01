# Generated by Django 4.2.6 on 2023-11-01 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0010_remove_organization_sector_organization_sub_sector_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="how_you_know_us",
            field=models.CharField(
                blank=True, default=None, max_length=120, null=True, verbose_name="Como nos conocio"
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="currency",
            field=models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name="Moneda"),
        ),
        migrations.AlterField(
            model_name="organizationmembership",
            name="expiration",
            field=models.DateField(verbose_name="Expiración de membresía"),
        ),
        migrations.AlterField(
            model_name="organizationmembership",
            name="is_active",
            field=models.BooleanField(
                default=False,
                help_text="Set to true when the user have an active membership.",
                verbose_name="Esta activa",
            ),
        ),
        migrations.AlterField(
            model_name="organizationmembership",
            name="start_date",
            field=models.DateField(blank=True, null=True, verbose_name="Inicio de membresía"),
        ),
    ]
