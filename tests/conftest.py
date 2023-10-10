import pytest

from backend.utils.managment_utils import load_data
from tests.utils.constants import TEST_DATA_PATH


@pytest.fixture(scope="session", autouse=True)
def configure_project(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        load_data(TEST_DATA_PATH)


@pytest.fixture
def drf_settings(settings):
    return getattr(settings, "REST_FRAMEWORK")


@pytest.fixture
def page_size(drf_settings):
    return drf_settings.get("PAGE_SIZE")
