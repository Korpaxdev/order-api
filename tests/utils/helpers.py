from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse
from faker import Faker

from backend.models import ProductShopModel
from tests.utils.constants import CONTENT_TYPE, ErrorMessages
from tests.utils.types import UserType


def assert_status_code(expected: HTTPStatus, actual: int):
    assert expected == actual, ErrorMessages.STATUS_CODE.format(expected, actual)


def assert_equal_data(expected, actual):
    assert expected == actual, ErrorMessages.DIFFERENT_DATA.format(expected, actual)


def assert_db_exists(value: any):
    assert value, ErrorMessages.EMPTY_DATABASE


def generate_address():
    fake = Faker("ru")
    address = {"postal_code": fake.postcode(), "country": fake.country(), "region": fake.word(), "city": fake.city()}
    return address


def generate_fake_user() -> UserType:
    fake = Faker("ru")
    user = {"username": fake.user_name(), "email": fake.email(), "password": fake.password()}
    return user


def create_test_order(client: Client):
    test_item: ProductShopModel = ProductShopModel.objects.filter(shop__status=True, quantity__gt=0).first()
    assert test_item, f"В базе данных нет тестового товара для создания заказа"
    test_data = {
        "address": generate_address(),
        "order_items": [{"product": test_item.product.pk, "shop": test_item.shop.pk, "quantity": 1}],
    }
    post_config = {"path": reverse("orders"), "content_type": CONTENT_TYPE, "data": test_data}
    return client.post(**post_config)


def create_test_user(client: Client, fake_user: UserType = None):
    fake_user = fake_user or generate_fake_user()
    post_config = {"path": reverse("register"), "content_type": CONTENT_TYPE, "data": fake_user}
    return client.post(**post_config)
