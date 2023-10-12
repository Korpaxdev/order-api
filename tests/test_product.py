from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse

from backend.models import ProductModel, ProductShopModel
from tests.utils.helpers import assert_db_exists, assert_equal_data, assert_status_code


class TestProduct:
    @pytest.mark.django_db
    def test_products_page(self, client: Client, page_size):
        """Тестирование страницы с товарами. Проверяется соответствие ответа с бд"""
        expected_products = (
            ProductModel.objects.filter(shops__status=True, productshopmodel__quantity__gt=0)
            .distinct()
            .values_list("name", flat=True)
            .order_by("name")[:page_size]
        )
        assert_db_exists(expected_products)
        response = client.get(reverse("products"))
        assert_status_code(HTTPStatus.OK, response.status_code)
        data = response.json()
        actual_products = [prod.get("name") for prod in data.get("results")]
        assert_equal_data(list(expected_products), actual_products)

    @pytest.mark.django_db
    def test_product_detail_page(self, client: Client):
        """Тестирование детальной информации о товаре. Так же проверяется соответствие такого товара в магазинах в бд"""
        first_product = ProductModel.objects.first()
        assert_db_exists(first_product)
        response = client.get(reverse("product_details_list", args=[first_product.slug]))
        assert_status_code(HTTPStatus.OK, response.status_code)
        data = response.json().get("results")
        assert len(data), f"Пустой результат детальной информации по продукту {first_product.name}"
        shop_names = [res.get("shop_name") for res in data]
        for shop in shop_names:
            assert ProductShopModel.objects.filter(
                product__name=first_product.name, shop__name=shop
            ).exists(), f"Продукта с именем {first_product.name} не существует в магазине {shop}"
