# Generated by Django 4.2.4 on 2023-08-28 10:37

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0015_alter_passwordresettokenmodel_options_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="OrderItemsModel",
            new_name="OrderItemModel",
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "Новый"),
                    ("confirmed", "Подтвержден"),
                    ("assembled", "Собран"),
                    ("sent", "Отправлен"),
                    ("delivered", "Доставлен"),
                    ("cancelled", "Отменен"),
                ],
                default="new",
                max_length=20,
                verbose_name="Статус заказа",
            ),
        ),
        migrations.AlterField(
            model_name="passwordresettokenmodel",
            name="expire",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 2, 13, 37, 47, 322923),
                verbose_name="Истекает",
            ),
        ),
        migrations.AlterField(
            model_name="productparametermodel",
            name="param",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="backend.parametermodel",
                verbose_name="Параметр",
            ),
        ),
    ]
