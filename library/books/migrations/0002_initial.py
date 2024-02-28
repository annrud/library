# Generated by Django 5.0.2 on 2024-02-25 13:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinhands',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books_in_hands', to=settings.AUTH_USER_MODEL, verbose_name='Посетитель'),
        ),
    ]