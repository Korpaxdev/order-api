from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse

from backend.models import OrderModel, ShopModel
from tests.utils.helpers import assert_db_exists, assert_equal_data, assert_status_code


class TestShop:
    @pytest.mark.django_db
    def test_shops_page(self, client: Client, page_size):
        """Тестирование страницы с магазинами. Проверяется соответствие результата с бд"""
        expected_shops = ShopModel.objects.all().order_by("name").values_list("name", flat=True)[:page_size]
        assert_db_exists(expected_shops)
        response = client.get(reverse("shops-list"))
        assert_status_code(HTTPStatus.OK, response.status_code)
        data = response.json()
        actual_shops = [res.get("name") for res in data.get("results")]
        assert_equal_data(list(expected_shops), actual_shops)

    @pytest.mark.django_db
    def test_shop_detail_page(self, client: Client):
        """Тестирование страницы с детальной информацией по магазину. Проверяется соответствие результата с бд"""
        first_shop: ShopModel = ShopModel.objects.first()
        assert_db_exists(first_shop)
        response = client.get(reverse("shops-detail", args=[first_shop.slug]))
        assert_status_code(HTTPStatus.OK, response.status_code)
        data = response.json()
        assert_equal_data(first_shop.name, data.get("name"))

    @pytest.mark.django_db
    def test_shop_price_list_page(self, client: Client, page_size):
        """Тестирование страницы с товарами в магазине. Проверяется соответствие результата с бд"""
        first_shop: ShopModel = ShopModel.objects.first()
        assert_db_exists(first_shop)
        response = client.get(reverse("shop_price_list", args=[first_shop.slug]))
        assert_status_code(HTTPStatus.OK, response.status_code)
        data = response.json()
        expected_products_names = list(
            first_shop.positions.all().order_by("product__name").values_list("product__name", flat=True)[:page_size]
        )
        actual_products_names = [res.get("product_name") for res in data.get("results")]
        assert_equal_data(expected_products_names, actual_products_names)

    @pytest.mark.django_db
    def test_shop_order_page(self, admin_client: Client):
        """Тестирование страницы с заказами магазина. Проверяется соответствие результата с бд"""
        first_shop: ShopModel = ShopModel.objects.first()
        assert_db_exists(first_shop)
        response = admin_client.get(reverse("shop_orders", args=[first_shop.slug]))
        assert_status_code(HTTPStatus.OK, response.status_code)
        expected_orders = list(
            OrderModel.objects.filter(items__position__shop__name=first_shop.name)
            .distinct()
            .order_by("id")
            .values_list("id", flat=True)
        )
        data = response.json()
        actual_orders = [res.get("id") for res in data.get("results")]
        assert_equal_data(expected_orders, actual_orders)

    @pytest.mark.django_db
    def test_change_shop_status(self, admin_client: Client):
        """Тестирование страницы по смене статуса магазина.
        Проверяется соответствие чтобы предыдущий статус не равен был новому"""
        first_shop: ShopModel = ShopModel.objects.first()
        assert_db_exists(first_shop)
        prev_status = first_shop.status
        response = admin_client.put(
            reverse("shop_update_status", args=[first_shop.slug]), {"status": False}, content_type="application/json"
        )
        assert_status_code(HTTPStatus.OK, response.status_code)
        first_shop.refresh_from_db()
        assert prev_status != first_shop.status, (
            f"Статус магазина {first_shop.name} не был изменен.\n"
            f"Expected status: {prev_status}\n"
            f"Actual status: {first_shop.status}"
        )
