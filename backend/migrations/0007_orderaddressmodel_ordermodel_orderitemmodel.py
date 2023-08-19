# Generated by Django 4.2.4 on 2023-08-19 10:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0006_alter_shopmodel_price_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderAddressModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("postal_code", models.IntegerField(verbose_name="Почтовый индекс")),
                ("country", models.CharField(max_length=100, verbose_name="Страна")),
                ("region", models.CharField(max_length=100, verbose_name="Область")),
                (
                    "city",
                    models.CharField(max_length=100, verbose_name="Населенный пункт"),
                ),
            ],
            options={
                "verbose_name": "Адрес доставки",
                "verbose_name_plural": "Адреса доставок",
            },
        ),
        migrations.CreateModel(
            name="OrderModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Новый"),
                            ("confirmed", "Подтвержден"),
                            ("assembled", "Собран"),
                            ("sent", "Отправлен"),
                            ("delivered", "Доставлен"),
                            ("canceled", "Отменен"),
                        ],
                        default="new",
                        max_length=20,
                        verbose_name="Статус заказа",
                    ),
                ),
                (
                    "additional",
                    models.TextField(verbose_name="Дополнительная информация"),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.orderaddressmodel",
                        verbose_name="Адрес доставки",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ пользователя",
                "verbose_name_plural": "Заказы пользователей",
            },
        ),
        migrations.CreateModel(
            name="OrderItemModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        default=1, verbose_name="Количество товара"
                    ),
                ),
                ("price", models.PositiveIntegerField(verbose_name="Цена товара")),
                (
                    "price_rrc",
                    models.PositiveIntegerField(
                        verbose_name="Рекомендованная розничная цена"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="backend.ordermodel",
                        verbose_name="Заказ",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.productshopmodel",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Позиция",
                "verbose_name_plural": "Позиции",
                "unique_together": {("order", "position")},
            },
        ),
    ]
