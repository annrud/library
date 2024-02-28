from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Visitor(AbstractUser):
    """Модель посетителя."""
    username = models.CharField(
        max_length=50,
        verbose_name=_('Логин'),
        null=True
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name=_('Имя')
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name=_('Фамилия')
    )
    address = models.CharField(
        max_length=200,
        verbose_name=_('Адрес проживания')
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_('Номер телефона'),
        unique=True
    )
    USERNAME_FIELD = 'phone'

    class Meta:
        ordering = ['id']
        verbose_name = _('Посетитель')
        verbose_name_plural = _('Посетители')

    def __str__(self):
        return self.get_full_name()
