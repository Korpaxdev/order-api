from dataclasses import dataclass


@dataclass(frozen=True)
class AuthErrors:
    AuthenticationFailed = "Ошибка авторизации. Проверьте access_token"
