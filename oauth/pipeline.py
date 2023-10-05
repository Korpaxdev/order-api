from rest_framework_simplejwt.tokens import RefreshToken


def generate_token(backend, user, response, *args, **kwargs):
    """
    В случае если есть redirect_url, то генерирует ему в параметры access и refresh токен
    Используется для redirect с токенами на стороннее приложение (например frontend)
    """
    redirect_url = backend.strategy.session_get("next")
    if redirect_url:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        params = f"?refresh={str(refresh)}&access={str(access)}"
        backend.strategy.session_set("next", redirect_url + params)
