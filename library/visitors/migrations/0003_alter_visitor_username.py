# Generated by Django 5.0.2 on 2024-02-28 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0002_alter_visitor_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='username',
            field=models.CharField(max_length=50, null=True, verbose_name='Логин'),
        ),
    ]