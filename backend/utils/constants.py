from dataclasses import dataclass

from django.conf import settings
from django.contrib.sites.models import Site

from backend.utils.types import ProductFieldType

SITE_DOMAIN = Site.objects.get_current().domain


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


@dataclass()
class EmailBaseSetup:
    subject: str
    template: str


@dataclass(frozen=True)
class EmailSendConfig:
    STATUS_CHANGE = EmailBaseSetup(subject="Ваш статус заказа был изменен",
                                   template="email_templates/change_order_status.html")
    PASSWORD_RESET = EmailBaseSetup(subject="Сброс пароля", template="email_templates/password_reset.html")
    PRICE_UPDATE = EmailBaseSetup(subject="Прайс файл успешно обновлен",
                                  template="email_templates/price_success_update.html")
    PRICE_UPDATE_ERROR = EmailBaseSetup(subject="Ошибка при обновлении прайса",
                                        template="email_templates/price_update_error.html")


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
    QUANTITY_GREATER_THAN_0 = "Количество товара в заказе должно быть больше 0"
    RESET_PASSWORD_EMAIL_ALREADY_SENT = 'Для пользователя с таким email уже было отправлено письмо для сброса пароля"'
    USER_WITH_EMAIL_NOT_FOUND = 'Пользователя с таким email не существует'
    PRODUCT_SHOP_UNIQUE_TOGETHER = "Поля product и shop вместе должны быть уникальными"
    SHOP_DOESNT_ACCEPT_ORDERS = "Указанный магазин не принимает заказы"
    PRICE_FILE_SERIALIZE_ERROR = "Ошибка при сериализации файла"
    PRICE_FILE_UNKNOWN_ERROR = "Неизвестная ошибка"
