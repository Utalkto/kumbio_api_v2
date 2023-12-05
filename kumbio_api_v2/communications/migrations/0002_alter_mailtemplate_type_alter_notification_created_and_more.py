# Generated by Django 4.2.6 on 2023-12-04 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("communications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailtemplate",
            name="type",
            field=models.IntegerField(choices=[(1, "Email"), (2, "Sms"), (3, "Whatsapp")], default=1),
        ),
        migrations.AlterField(
            model_name="notification",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, help_text="Date time on which the object was created.", verbose_name="created at"
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="modified",
            field=models.DateTimeField(
                auto_now=True, help_text="Date time on which the object was last modified.", verbose_name="modified at"
            ),
        ),
    ]