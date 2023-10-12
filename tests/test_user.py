from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse

from backend.models import OrderModel, UserModel
from tests.utils.constants import CONTENT_TYPE, ErrorMessages
from tests.utils.helpers import (
    assert_equal_data,
    assert_status_code,
    create_test_order,
    create_test_user,
    generate_fake_user,
)
from tests.utils.types import UserType


class TestUser:
    @pytest.mark.django_db
    def test_profile_page(self, admin_client: Client, client: Client):
        """Тестирование страницы с профилем. Проверяется соответствие результата с бд"""
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
        """Тестирование страницы с созданием заказа. Проверяется наличие созданного заказа в бд"""
        admin_response = create_test_order(admin_client)
        assert_status_code(HTTPStatus.CREATED, admin_response.status_code)
        data = admin_response.json()
        order = OrderModel.objects.filter(user=admin_user, id=data.get("id")).first()
        assert order, f"Заказ не был создан в базе данных\n" f"Expected: {data}\n" f"Actual: {order}"
        unauthorized_response = create_test_order(client)
        assert_status_code(HTTPStatus.UNAUTHORIZED, unauthorized_response.status_code)

    @pytest.mark.django_db
    def test_create_user(self, client: Client):
        """Тестирование страницы с регистрацией пользователя. Проверяется наличие созданного пользователя в бд"""
        response = create_test_user(client)
        assert_status_code(HTTPStatus.CREATED, response.status_code)
        data = response.json()
        username = data.get("username")
        user = UserModel.objects.filter(username=username).first()
        assert user, ErrorMessages.USER_NOT_FOUND.format(username)

    @pytest.mark.django_db
    def test_get_user_token(self, client: Client):
        """Тестирование страницы с получением токена. Проверяется чтобы в ответе был access и refresh токены"""
        fake_user: UserType = generate_fake_user()
        create_user_response = create_test_user(client, fake_user)
        assert_status_code(HTTPStatus.CREATED, create_user_response.status_code)
        post_config = {"path": reverse("token"), "content_type": CONTENT_TYPE, "data": fake_user}
        token_response = client.post(**post_config)
        assert_status_code(HTTPStatus.OK, token_response.status_code)
        token_data = token_response.json()
        assert token_data.get("access") and token_data.get("refresh"), ErrorMessages.WRONG_TOKEN_RESPONSE.format(
            token_data
        )
