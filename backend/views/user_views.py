from django.http import HttpRequest
from rest_framework import generics, permissions
from rest_framework.response import Response

from backend.models import UserModel
from backend.serializers.user_serializers import UserSerializer


class UserProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request: HttpRequest):
        user = request.user
        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
