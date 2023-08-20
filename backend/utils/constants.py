from dataclasses import dataclass

from django.conf import settings

from backend.utils.types import ProductFieldType


@dataclass(frozen=True)
class Validation:
    REQUIRED = "REQUIRED"
    IS_NUMBER = "IS_NUMBER"


PRODUCT_FIELDS: list[ProductFieldType] = [
    {"name": "name", "validation": [Validation.REQUIRED]},
    {"name": "categories", "validation": [Validation.REQUIRED]},
    {"name": "price", "validation": [Validation.REQUIRED, Validation.IS_NUMBER]},
    {"name": "price_rrc", "validation": [Validation.REQUIRED, Validation.IS_NUMBER]},
    {
        "name": "quantity",
        "validation": [Validation.REQUIRED, Validation.IS_NUMBER],
    },
]


@dataclass(frozen=True)
class ErrorMessages:
    PRICE_FILE_INCORRECT_FILE = "Прайс файл должен содержать список товаров"
    PRICE_FILE_NOT_A_NUMBER = "Поле %s должно быть числом"
    PRICE_FILE_REQUIRED_FIELD = "Поле %s обязательно для заполнения"
    PRICE_FILE_INCORRECT_FORMAT = "Недопустимый формат файла. Допустимые форматы: %s" % ",".join(
        settings.PRICE_FILE_FORMATS
    )
    CANT_SET_STATUS = "Невозможно установить статус %s, когда у магазина отсутствует прайс файл"
    PRODUCT_WITH_ID_NOT_FOUND = "Товара с таким id не существует"
    SHOP_WITH_ID_NOT_FOUND = "Магазина с таким id не существует"
    POSITION_WITH_ID_NOT_FOUND = "Позиции с таким product_id и shop_id не существует"
    POSITION_IS_OUT_OF_STOCK = "Такой позиции сейчас нет в наличии в магазине"
    LESSER_QUANTITY = "Количество товара в магазине меньше чем указанное количество в заказе"
    USER_EMAIL_IS_EXIST = "Такой email уже используется"
