import os

import yaml
from celery import shared_task

from backend.models import CategoryModel, ParameterModel, ProductModel, ProductParameterModel, ShopModel
from backend.utils.managment_utils import dump_data, load_data
from backend.utils.price_file_utils import set_all_position_to_0, get_fixtures_paths, validate_price_data


@shared_task
def remove_file(filepath: str):
    print(filepath)
    os.remove(filepath)


@shared_task
def update_price_file(shop_id: int, price_file: str):
    print(price_file)
    shop = ShopModel.objects.get(pk=shop_id)
    fixtures = get_fixtures_paths(shop.pk)
    try:

        pos_ids = []
        pos_ids_params = []

        for position in shop.positions.all():
            pos_ids.append(position.pk)
            for parameter in position.product_parameters.all():
                pos_ids_params.append(parameter.pk)

        dump_data("backend.ProductShopModel", output=fixtures['product'], primary_keys=pos_ids)

        dump_data("backend.ProductParameterModel", output=fixtures['product_param'], primary_keys=pos_ids_params)

        set_all_position_to_0(shop)

        with open(price_file, "r") as f:
            price_data = yaml.safe_load(f)
            product_list = validate_price_data(price_data)

            for price_product in product_list:
                cats = []

                for price_category in price_product["categories"]:
                    category, _ = CategoryModel.objects.get_or_create(name=price_category)
                    cats.append(category)

                product, _ = ProductModel.objects.get_or_create(name=price_product["name"])
                product.categories.add(*cats)

                position, _ = shop.positions.update_or_create(
                    product=product,
                    shop=shop,
                    defaults={
                        'description': price_product.get("description", ""),
                        'quantity': price_product["quantity"],
                        'price': price_product["price"],
                        'price_rrc': price_product['price_rrc']
                    }

                )

                for price_param in price_product.get("params", []):
                    for price_param_name, price_param_value in price_param.items():
                        param, _ = ParameterModel.objects.get_or_create(name=price_param_name)
                        product_param, _ = ProductParameterModel.objects.update_or_create(
                            product=position, param=param, value=price_param_value
                        )

                print(f"Updated {product.name}")

        for fixture in fixtures.values():
            remove_file.delay(fixture)

    except Exception as e:
        set_all_position_to_0(shop)
        for fixture in fixtures.values():
            load_data(fixture)
            remove_file.delay(fixture)
        print(f"Restore backup for {shop.name} {shop.pk}")
        raise e
