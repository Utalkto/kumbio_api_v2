from django.db import models

from kumbio_api_v2.utils.models import KumbioModel


class MailTemplate(KumbioModel):
    """Mail templates model."""
    class MessageChannel(models.TextChoices):
        """Message channel type."""

        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "Sms"
        WHATSAPP = "WHATSAPP", "Whatsapp"

    name = models.CharField('Nombre de la plantilla', max_length=120)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    message_type = models.IntegerField(choices=MessageChannel.choices, default=MessageChannel.EMAIL)

    def __str__(self):
        return f"{self.pk} - {self.name}"
    


# class TranslateMetaVariable(HackuModelBase):
#     class Variables(models.TextChoices):
#         # Variables for whatsapp official
#         OFFICIAL_1 = '1', '{{1}}'
#         OFFICIAL_2 = '2', '{{2}}'
#         OFFICIAL_3 = '3', '{{3}}'
#         OFFICIAL_4 = '4', '{{4}}'
#         OFFICIAL_5 = '5', '{{5}}'
#         OFFICIAL_6 = '6', '{{6}}'
#         OFFICIAL_7 = '7', '{{7}}'
#         OFFICIAL_8 = '8', '{{8}}'
#         OFFICIAL_9 = '9', '{{9}}'
#         OFFICIAL_10 = '10', '{{10}}'
#         OFFICIAL_11 = '11', '{{11}}'
#         OFFICIAL_12 = '12', '{{12}}'

#     variant = models.ForeignKey(HsmMetaVariant, on_delete=models.CASCADE, related_name='vars')
#     variable_type = models.CharField(
#         max_length=55,
#         choices=Variables.choices,
#     )
#     translate = models.CharField(max_length=55)
#     is_url = models.BooleanField(default=False)
#     required = models.BooleanField(
#         help_text="Set to true when the variable is required.",
#         default=False
#     )

#     def __str__(self):
#         return f'Variable translate: {self.variable_type}'

# class VariablesMessage(KumbioModel):
#     """Variables template model."""

#     class Variables(models.TextChoices):
#         # Variables for whatsapp official
#         OFFICIAL_1 = '1', '{{1}}'
#         OFFICIAL_2 = '2', '{{2}}'
#         OFFICIAL_3 = '3', '{{3}}'
#         OFFICIAL_4 = '4', '{{4}}'
#         OFFICIAL_5 = '5', '{{5}}'
#         OFFICIAL_6 = '6', '{{6}}'
#         OFFICIAL_7 = '7', '{{7}}'
#         OFFICIAL_8 = '8', '{{8}}'
#         OFFICIAL_9 = '9', '{{9}}'
#         OFFICIAL_10 = '10', '{{10}}'
#         OFFICIAL_11 = '11', '{{11}}'
#         OFFICIAL_12 = '12', '{{12}}'

#     variable_type = models.CharField(
#         max_length=55,
#         choices=Variables.choices,
#     )
#     translate = models.CharField(max_length=55)
