from dataclasses import dataclass

TEST_DATA_PATH = "tests/test_data/data.json"


@dataclass(frozen=True)
class ErrorMessages:
    STATUS_CODE = "Статус ответа отличный от {0}.\nExpected: {0}\nActual: {1}"
    DIFFERENT_DATA = "Полученные данные отличаются от ожидаемых.\nExpected: {0}\nActual: {1}"
    EMPTY_DATABASE = "База данных не заполнена для этого теста"
