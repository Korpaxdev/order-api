# Generated by Django 4.2.4 on 2023-08-13 13:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0004_categorymodel_parametermodel_productmodel_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ProductParameter",
            new_name="ProductParameterModel",
        ),
    ]
