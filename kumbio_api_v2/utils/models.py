"""Django models utilities."""

# Django
from django.db import models


class KumbioModel(models.Model):
    """Training base model.
    TrainingModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField("created at", auto_now_add=True, help_text="Date time on which the object was created.")
    modified = models.DateTimeField("modified at", auto_now=True, help_text="Date time on which the object was last modified.")

    class Meta:
        """Meta option."""

        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class DaysChoices(models.TextChoices):
    MONDAY = "MONDAY", "Lunes"
    TUESDAY = "TUESDAY", "Martes"
    WEDNESDAY = "WEDNESDAY", "Miércoles"
    THURSDAY = "THURSDAY", "Jueves"
    FRIDAY = "FRIDAY", "Viernes"
    SATURDAY = "SATURDAY", "Sábado"
    SUNDAY = "SUNDAY", "Domingo"


weekdays = [
    DaysChoices.MONDAY,
    DaysChoices.TUESDAY,
    DaysChoices.WEDNESDAY,
    DaysChoices.THURSDAY,
    DaysChoices.FRIDAY,
    DaysChoices.SATURDAY,
    DaysChoices.SUNDAY,
]
