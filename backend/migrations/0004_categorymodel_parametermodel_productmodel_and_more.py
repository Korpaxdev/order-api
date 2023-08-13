# Generated by Django 4.2.4 on 2023-08-13 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0003_usermanagermodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryModel",
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
                    "name",
                    models.CharField(max_length=50, unique=True, verbose_name="Название категории"),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="ParameterModel",
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
                    "name",
                    models.CharField(max_length=50, unique=True, verbose_name="Название параметра"),
                ),
            ],
            options={
                "verbose_name": "Параметр",
                "verbose_name_plural": "Параметры",
            },
        ),
        migrations.CreateModel(
            name="ProductModel",
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
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Название товара"),
                ),
                (
                    "slug",
                    models.SlugField(blank=True, max_length=100, null=True, unique=True),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="products",
                        to="backend.categorymodel",
                        verbose_name="Категории товара",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
        migrations.CreateModel(
            name="ProductShopModel",
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
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание товара"),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(verbose_name="Количество товара"),
                ),
                ("price", models.PositiveIntegerField(verbose_name="Цена товара")),
                (
                    "price_rrc",
                    models.PositiveIntegerField(verbose_name="Рекомендованная розничная цена товара"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.productmodel",
                        verbose_name="Товар",
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="positions",
                        to="backend.shopmodel",
                        verbose_name="Магазин",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар в магазинах",
                "verbose_name_plural": "Товары в магазинах",
                "unique_together": {("product", "shop")},
            },
        ),
        migrations.CreateModel(
            name="ProductParameter",
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
                    "value",
                    models.CharField(max_length=50, verbose_name="Значение параметра"),
                ),
                (
                    "param",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.parametermodel",
                        verbose_name="Параметр",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_parameters",
                        to="backend.productshopmodel",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Параметр товара",
                "verbose_name_plural": "Параметры товара",
            },
        ),
        migrations.AddField(
            model_name="productmodel",
            name="shops",
            field=models.ManyToManyField(
                through="backend.ProductShopModel",
                to="backend.shopmodel",
                verbose_name="Магазины",
            ),
        ),
    ]
