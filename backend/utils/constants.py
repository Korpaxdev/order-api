from dataclasses import dataclass

from backend.utils.types import ProductFieldType


@dataclass(frozen=True)
class PriceFileMessages:
    REQUIRED_FIELD = "Поле %s обязательно для заполнения"
    NOT_A_NUMBER = "Поле %s должно быть числом"
    INCORRECT_FILE = "Прайс файл должен содержать список товаров"


@dataclass(frozen=True)
class Validation:
    REQUIRED = 'REQUIRED'
    IS_NUMBER = 'IS_NUMBER'


PRODUCT_FIELDS: list[ProductFieldType] = [
    {
        'name': 'name',
        'validation': [Validation.REQUIRED]
    },
    {
        'name': 'categories',
        'validation': [Validation.REQUIRED]
    },
    {
        'name': 'price',
        'validation': [Validation.REQUIRED, Validation.IS_NUMBER]
    },
    {
        'name': 'price_rrc',
        'validation': [Validation.REQUIRED, Validation.IS_NUMBER]
    },
    {
        'name': 'quantity',
        'validation': [Validation.REQUIRED, Validation.IS_NUMBER],
    },
]
