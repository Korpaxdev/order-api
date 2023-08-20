import uuid

from django.conf import settings

from backend.models import ShopModel
from backend.utils.constants import PRODUCT_FIELDS, ErrorMessages, Validation
from backend.utils.exceptions import PriceFileException
from backend.utils.types import FixturesPathsType, ProductType


def ids_to_string(ids: list | str) -> str:
    if isinstance(ids, list):
        try:
            return ",".join(ids)
        except TypeError:
            ids = [str(pk) for pk in ids]
            return ",".join(ids)
    return ids


def get_fixtures_paths(shop_id: int) -> FixturesPathsType:
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
    return f"shop-{shop_id}-{uuid.uuid4()}.json"


def set_all_position_to_0(shop: ShopModel):
    shop.positions.all().update(quantity=0)
    print(f"set all positions to 0 for shop {shop.id}")


def validate_product(product: dict):
    for field in PRODUCT_FIELDS:
        if Validation.REQUIRED in field["validation"] and not product.get(field["name"]):
            raise PriceFileException(ErrorMessages.PRICE_FILE_REQUIRED_FIELD % field["name"])
        if Validation.IS_NUMBER in field["validation"] and not isinstance(product.get(field["name"]), int):
            raise PriceFileException(ErrorMessages.PRICE_FILE_NOT_A_NUMBER % field["name"])


def validate_price_data(price_data: any) -> list[ProductType]:
    if not isinstance(price_data, list):
        raise PriceFileException(ErrorMessages.PRICE_FILE_INCORRECT_FILE)
    for product in price_data:
        validate_product(product)
    return price_data
