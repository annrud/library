from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    """Модель отдела."""
    name = models.CharField(
        max_length=50,
        verbose_name=_('Название отдела')
    )
