from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
)

from backend.utils.constants import PRODUCT_FIELDS, Validation, ErrorMessages
from backend.utils.exceptions import PriceFileException
from backend.utils.types import ProductType


def password_validation(password: str):
    validators = [MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator]
    for validator in validators:
        validator().validate(password)


def product_validation(product: dict):
    """Валидация на корректность заполнения product из price_file"""
    for field in PRODUCT_FIELDS:
        if Validation.REQUIRED in field["validation"] and not product.get(field["name"]):
            raise PriceFileException(ErrorMessages.PRICE_FILE_REQUIRED_FIELD % field["name"])
        if Validation.IS_NUMBER in field["validation"] and not isinstance(product.get(field["name"]), int):
            raise PriceFileException(ErrorMessages.PRICE_FILE_NOT_A_NUMBER % field["name"])


def price_data_validation(price_data: any) -> list[ProductType]:
    """Валидация корректности заполнения price_file"""
    if not isinstance(price_data, list):
        raise PriceFileException(ErrorMessages.PRICE_FILE_INCORRECT_FILE)
    for product in price_data:
        product_validation(product)
    return price_data
