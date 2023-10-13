# Generated by Django 4.2.6 on 2023-10-13 04:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="first name"),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="last name"),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
