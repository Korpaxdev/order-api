import pytest

from backend.tasks.testing_tasks import disable_send_email
from backend.utils.managment_utils import load_data
from tests.utils.constants import TEST_DATA_PATH


@pytest.fixture(scope="session", autouse=True)
def configure_project(django_db_setup, django_db_blocker):
    """Фикстура для загрузки тестовых данных в бд. Дополнительно устанавливаем SEND_EMAIL в окружении celery в False"""
    disable_send_email.delay().get()
    with django_db_blocker.unblock():
        load_data(TEST_DATA_PATH)


@pytest.fixture
def drf_settings(settings):
    """Фикстура, которая возвращает настройки REST_FRAMEWORK"""
    return getattr(settings, "REST_FRAMEWORK")


@pytest.fixture
def page_size(drf_settings):
    """Фикстура, которая возвращает настройку PAGE_SIZE из REST_FRAMEWORK settings"""
    return drf_settings.get("PAGE_SIZE")
