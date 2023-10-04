from django.http import HttpRequest
from django.urls import reverse
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy

from oauth.serializers import AuthByAccessTokenSerializer


class AuthByAccessTokenView(generics.GenericAPIView):
    """Авторизация по access_token через backend"""

    serializer_class = AuthByAccessTokenSerializer

    def post(self, request: HttpRequest, backend: str):
        self.request.social_strategy = load_strategy(self.request)
        if not hasattr(self.request, "strategy"):
            self.request.strategy = self.request.social_strategy
        try:
            self.request.backend = load_backend(
                self.request.social_strategy, backend, redirect_uri=reverse("social:complete", args=[backend])
            )
        except MissingBackend:
            raise NotFound("Такой backend не найден")
        serializer = self.serializer_class(data=self.request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
