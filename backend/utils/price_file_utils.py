import uuid

from django.conf import settings

from backend.models import ShopModel
from backend.utils.types import FixturesPathsType


def ids_to_string(ids: list | str) -> str:
    """Создает строку из списка переданных ids"""
    if isinstance(ids, list):
        try:
            return ",".join(ids)
        except TypeError:
            ids = [str(pk) for pk in ids]
            return ",".join(ids)
    return ids


def get_fixtures_paths(shop_id: int) -> FixturesPathsType:
    """Задает пути для хранения fixtures"""
    fixture_name = gen_fixture_name(shop_id)
    products_fixtures_path = settings.PRICE_FILE_BACKUP_FIXTURES / "products"
    product_params_fixtures_path = settings.PRICE_FILE_BACKUP_FIXTURES / "shops"
    for path in [products_fixtures_path, product_params_fixtures_path]:
        path.mkdir(parents=True, exist_ok=True)
    fixtures: FixturesPathsType = {
        "product": str(products_fixtures_path / fixture_name),
        "product_param": str(product_params_fixtures_path / fixture_name),
    }
    return fixtures


def gen_fixture_name(shop_id: int):
    """Генерирует имя fixture на основе shop_id"""
    return f"shop-{shop_id}-{uuid.uuid4()}.json"


def set_all_position_to_0(shop: ShopModel):
    """Устанавливает количество всех позиций модели ShopModel в 0"""
    shop.positions.all().update(quantity=0)
    print(f"set all positions to 0 for shop {shop.id}")
