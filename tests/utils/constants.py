from dataclasses import dataclass

TEST_DATA_PATH = "tests/test_data/data.json"
CONTENT_TYPE = "application/json"


@dataclass(frozen=True)
class ErrorMessages:
    STATUS_CODE = "Статус ответа отличный от {0}.\nExpected: {0}\nActual: {1}"
    DIFFERENT_DATA = "Полученные данные отличаются от ожидаемых.\nExpected: {0}\nActual: {1}"
    EMPTY_DATABASE = "База данных не заполнена для этого теста"
    USER_NOT_FOUND = "Пользователь с таким username {0} Не найден"
    WRONG_TOKEN_RESPONSE = (
        'В ответе нет access и refresh токенов.\nExpected: {{"access":str, "refresh":str}}\nActual: {0}'
    )
