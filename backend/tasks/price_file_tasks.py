import os

import yaml
from celery import shared_task

from backend.models import CategoryModel, ParameterModel, ProductModel, ProductParameterModel, ShopModel
from backend.tasks.email_tasks import send_price_error_update_email, send_price_success_updated_email
from backend.utils.constants import ErrorMessages
from backend.utils.exceptions import PriceFileException
from backend.utils.managment_utils import dump_data, load_data
from backend.utils.price_file_utils import get_fixtures_paths, set_all_position_to_0
from backend.utils.types import FixturesPathsType
from backend.utils.validation import price_data_validation


@shared_task
def remove_file_task(filepath: str):
    """Удаляет файл по пути filepath"""
    print(filepath)
    os.remove(filepath)


@shared_task
def update_price_file_task(shop_id: int, price_file: str, user_id: int):
    """Обновляет модели товаров на основе price_file"""
    shop = ShopModel.objects.get(pk=shop_id)
    fixtures = get_fixtures_paths(shop.pk)
    try:
        pos_ids = []
        pos_ids_params = []

        for position in shop.positions.all():
            pos_ids.append(position.pk)
            for parameter in position.product_parameters.all():
                pos_ids_params.append(parameter.pk)

        dump_data("backend.ProductShopModel", output=fixtures["product"], primary_keys=pos_ids)

        dump_data("backend.ProductParameterModel", output=fixtures["product_param"], primary_keys=pos_ids_params)

        set_all_position_to_0(shop)

        with open(price_file, "r") as f:
            price_data = yaml.safe_load(f)
            product_list = price_data_validation(price_data)

            for price_product in product_list:
                cats = []

                for price_category in price_product["categories"]:
                    category, _ = CategoryModel.objects.get_or_create(name__iexact=price_category,
                                                                      defaults={"name": price_category})
                    cats.append(category)

                product, _ = ProductModel.objects.get_or_create(name__iexact=price_product["name"],
                                                                defaults={'name': price_product['name']})
                product.categories.add(*cats)

                position, _ = shop.positions.update_or_create(
                    product=product,
                    shop=shop,
                    defaults={
                        "description": price_product.get("description", ""),
                        "quantity": price_product["quantity"],
                        "price": price_product["price"],
                        "price_rrc": price_product["price_rrc"],
                    },
                )

                position.product_parameters.all().delete()

                for price_param in price_product.get("params", []):
                    for price_param_name, price_param_value in price_param.items():
                        param, _ = ParameterModel.objects.get_or_create(name__iexact=price_param_name,
                                                                        defaults={'name': price_param_name})
                        product_param, _ = ProductParameterModel.objects.update_or_create(
                            product=position, param=param, value=price_param_value,
                        )

                print(f"Updated {product.name}")

        for fixture in fixtures.values():
            remove_file_task.delay(fixture)

        send_price_success_updated_email.delay(user_id, shop_id)
    except PriceFileException as e:
        restore_backup(shop, fixtures)
        send_price_error_update_email.delay(user_id, shop_id, str(e))
        raise e
    except Exception as e:
        restore_backup(shop, fixtures)
        send_price_error_update_email.delay(user_id, shop_id, ErrorMessages.PRICE_FILE_UNKNOWN_ERROR)
        raise e


def restore_backup(shop: ShopModel, fixtures: FixturesPathsType):
    """Восстанавливает backup из fixtures для магазина shop"""
    set_all_position_to_0(shop)
    for fixture in fixtures.values():
        load_data(fixture)
        remove_file_task.delay(fixture)
    print(f"Restore backup for {shop.name} {shop.pk}")
