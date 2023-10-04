from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse
from faker import Faker

from backend.models import ProductShopModel
from tests.constants import ErrorMessages


def assert_status_code(expected: HTTPStatus, actual: int):
    assert expected == actual, ErrorMessages.STATUS_CODE.format(expected, actual)


def assert_equal_data(expected, actual):
    assert expected == actual, ErrorMessages.DIFFERENT_DATA.format(expected, actual)


def assert_exist(value: any):
    assert value, ErrorMessages.EMPTY_DATABASE


def generate_address():
    fake = Faker("ru")
    address = {"postal_code": fake.postcode(), "country": fake.country(), "region": fake.word(), "city": fake.city()}
    return address


def create_test_order(client: Client):
    test_item: ProductShopModel = ProductShopModel.objects.filter(shop__status=True, quantity__gt=0).first()
    assert test_item, f"В базе данных нет тестового товара для создания заказа"
    test_data = {
        "address": generate_address(),
        "order_items": [{"product": test_item.product.pk, "shop": test_item.shop.pk, "quantity": 1}],
    }
    post_config = {"path": reverse("orders"), "content_type": "application/json", "data": test_data}
    return client.post(**post_config)
