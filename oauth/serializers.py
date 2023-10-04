from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.exceptions import AuthException, AuthTokenRevoked

from oauth.utils.constants import AuthErrors


class AuthByAccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        write_only=True,
        required=True,
    )
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context["request"]
        try:
            user = request.backend.do_auth(data["access_token"])
            if not user:
                raise exceptions.AuthenticationFailed(AuthErrors.AuthenticationFailed)
            refresh = RefreshToken.for_user(user)
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
        except (AuthTokenRevoked, AuthException):
            raise exceptions.AuthenticationFailed(AuthErrors.AuthenticationFailed)
        return data
