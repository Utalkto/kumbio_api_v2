# Generated by Django 4.2.6 on 2023-12-05 13:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("communications", "0005_queuemessage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailtemplate",
            name="slug_name",
        ),
    ]