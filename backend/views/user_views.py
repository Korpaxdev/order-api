from django.http import HttpRequest
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import OrderItemModel, OrderModel, PasswordResetTokenModel, UserModel
from backend.serializers.user_serializers import (
    OrderDetailSerializer,
    OrderPositionSerializer,
    OrderSerializer,
    UserPasswordResetTokenSerializer,
    UserSerializer,
    UserUpdatePasswordSerializer,
)
from backend.tasks.email_tasks import send_password_reset_email


class UserProfileView(generics.GenericAPIView):
    """View класс для представления авторизованного пользователя UserModel
    Url: users/profile/"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request: HttpRequest):
        user = request.user
        serializer = self.serializer_class(user, context={"request": request})
        return Response(serializer.data)


class UserRegisterView(generics.CreateAPIView):
    """View класс для создания объекта модели UserModel
    Url: users/register/"""
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()


class UserOrdersView(generics.ListCreateAPIView):
    """View класс для представления списка объектов модели OrderModel
    Url: users/profile/orders/"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)


class UserOrderDetailView(generics.RetrieveAPIView):
    """View класс для представления детальной информации об объекте модели OrderModel
    Url: users/profile/orders/<int:order>/"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderDetailSerializer
    lookup_url_kwarg = "order"

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).prefetch_related("items__position")


class UserOrderPositionsView(generics.ListAPIView):
    """View класс для представления списка объектов из модели OrderItemModel
    Url: users/profile/orders/<int:order>/items/"""
    permissions = (permissions.IsAuthenticated,)
    serializer_class = OrderPositionSerializer
    lookup_url_kwarg = "order"

    def get_queryset(self):
        return (
            OrderItemModel.objects.filter(order=self.kwargs["order"], order__user=self.request.user)
            .select_related("position__product", "position__shop")
            .prefetch_related("position__product__categories", "position__product_parameters__param")
        )


class CreateUserPasswordResetView(generics.GenericAPIView):
    """View класс для создания объекта модели PasswordResetTokenModel
    Url: users/password/reset"""
    serializer_class = UserPasswordResetTokenSerializer
    queryset = PasswordResetTokenModel

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(validated_data=serializer.validated_data)
        send_password_reset_email.delay(instance.pk)
        return Response(
            {
                "detail": f"Email со ссылкой для сброса пароля было отправлено на указанный email адрес. Ссылка будет активна до: {instance.expire}"
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class UserPasswordUpdateView(generics.GenericAPIView):
    """View класс для обновления поля password у объекта модели UserModel
    Url: users/password/update/<str:user>/<uuid:token>/"""
    serializer_class = UserUpdatePasswordSerializer
    queryset = UserModel.objects.all()

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, username=kwargs.get("user"))
        token = get_object_or_404(PasswordResetTokenModel, token=kwargs.get("token"), user=user)
        serializer = UserUpdatePasswordSerializer(data=self.request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token.delete()
        return Response(serializer.data)
