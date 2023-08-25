# Generated by Django 4.2.4 on 2023-08-24 11:53

import datetime
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0014_alter_orderitemsmodel_position_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="passwordresettokenmodel",
            options={
                "verbose_name": "Токен для сброса пароля",
                "verbose_name_plural": "Токены для сброса пароля",
            },
        ),
        migrations.AlterField(
            model_name="passwordresettokenmodel",
            name="expire",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 8, 29, 14, 53, 38, 602395),
                verbose_name="Истекает",
            ),
        ),
        migrations.AlterField(
            model_name="passwordresettokenmodel",
            name="token",
            field=models.UUIDField(default=uuid.uuid4, verbose_name="Токен"),
        ),
        migrations.AlterField(
            model_name="passwordresettokenmodel",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
