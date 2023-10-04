from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse

from backend.models import OrderModel, ProductShopModel, UserModel
from tests.utils import assert_equal_data, assert_status_code, create_test_order, generate_address


class TestUser:
    @pytest.mark.django_db
    def test_profile_page(self, admin_client: Client, client: Client):
        admin: UserModel = UserModel.objects.filter(is_superuser=True, username="admin").first()
        assert admin, "Не создан суперпользователь"
        profile_url = reverse("profile")
        admin_response = admin_client.get(profile_url)
        assert_status_code(HTTPStatus.OK, admin_response.status_code)
        data = admin_response.json()
        for key in ["username", "email"]:
            assert_equal_data(getattr(admin, key), data.get(key))
        unauthorized_response = client.get(profile_url)
        assert_status_code(HTTPStatus.UNAUTHORIZED, unauthorized_response.status_code)

    @pytest.mark.django_db
    def test_create_order_page(self, admin_client: Client, admin_user, client: Client):
        admin_response = create_test_order(admin_client)
        assert_status_code(HTTPStatus.CREATED, admin_response.status_code)
        data = admin_response.json()
        order = OrderModel.objects.filter(user=admin_user, id=data.get("id")).first()
        assert order, f"Не был создан заказ в базе данных\n" f"Expected: {data}\n" f"Actual: {order}"
        unauthorized_response = create_test_order(client)
        assert_status_code(HTTPStatus.UNAUTHORIZED, unauthorized_response.status_code)

    @pytest.mark.django_db
    def test_order_list_page(self, admin_client: Client, admin_user, client: Client):
        orders_ids = OrderModel.objects.all()
        print(orders_ids)
