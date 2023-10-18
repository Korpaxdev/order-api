from django.http import HttpRequest
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.filters.order_filters import OrderListFilterSet
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
    """Получение информации о текущем авторизованном пользователе."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request: HttpRequest):
        user = request.user
        serializer = self.serializer_class(user, context={"request": request})
        return Response(serializer.data)


class UserRegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""

    serializer_class = UserSerializer
    queryset = UserModel.objects.all()


class UserOrdersView(generics.ListCreateAPIView):
    """Получение и создание списка заказов авторизованного пользователя"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderSerializer
    filterset_class = OrderListFilterSet

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return OrderModel.objects.none()
        return OrderModel.objects.filter(user=self.request.user)


class UserOrderDetailView(generics.RetrieveAPIView):
    """Получение детальной информации о заказе"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderDetailSerializer
    lookup_url_kwarg = "order"

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).prefetch_related("items__position")


class UserOrderPositionsView(generics.ListAPIView):
    """Получение списка товаров в заказе {order}"""

    permissions = (permissions.IsAuthenticated,)
    serializer_class = OrderPositionSerializer
    lookup_url_kwarg = "order"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return OrderModel.objects.none()

        return (
            OrderItemModel.objects.filter(order=self.kwargs.get("order"), order__user=self.request.user)
            .select_related("position__product", "position__shop")
            .prefetch_related("position__product__categories", "position__product_parameters__param")
        )


class CreateUserPasswordResetView(generics.GenericAPIView):
    """Сброс пароля пользователя по email"""

    serializer_class = UserPasswordResetTokenSerializer
    queryset = PasswordResetTokenModel

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(validated_data=serializer.validated_data)
        send_password_reset_email.delay(instance.pk)
        return Response(
            {
                "detail": f"Email со ссылкой для сброса пароля было отправлено на указанный email адрес. "
                f"Ссылка будет активна до: {instance.expire}"
            },
            status=status.HTTP_200_OK,
        )


class UserPasswordUpdateView(generics.GenericAPIView):
    """Обновление пароля для пользователя {user} по токену {token}"""

    serializer_class = UserUpdatePasswordSerializer
    queryset = UserModel.objects.all()

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, username=kwargs.get("user"))
        token = get_object_or_404(PasswordResetTokenModel, token=kwargs.get("token"), user=user)
        if token.expire < timezone.localtime():
            return Response({"detail": "Токен истек"}, status.HTTP_400_BAD_REQUEST)
        serializer = UserUpdatePasswordSerializer(data=self.request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token.delete()
        return Response(serializer.data)
