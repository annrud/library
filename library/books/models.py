from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from departments.models import Department

Visitor = get_user_model()


class Book(models.Model):
    """Модель книги."""
    title = models.CharField(
        max_length=150,
        verbose_name=_('Название')
        )
    author = models.CharField(
        max_length=100,
        verbose_name=_('Автор')
        )
    year = models.SmallIntegerField(verbose_name=_('Год издания'))
    count = models.SmallIntegerField(
        verbose_name=_('Количество экземпляров')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name='books',
        verbose_name=_('Отдел'),
        null=True
    )

    def __str__(self):
        return f'{self.author} {self.title}'


class BookInHands(models.Model):
    """Модель записи о выдаче посетителю книги."""
    visitor = models.ForeignKey(
        Visitor, on_delete=models.PROTECT,
        related_name='books_in_hands',  verbose_name=_('Посетитель')
    )
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT,
        related_name='books_in_hands', verbose_name=_('Книга')
    )
    borrow_date = models.DateField(
        auto_now_add=True, verbose_name=_('Дата выдачи')
    )
    return_date = models.DateField(null=True, verbose_name=_('Дата возврата'))

    def __str__(self):
        return f'{self.visitor} - {self.book}'
