from django.http import HttpRequest
from rest_framework import generics, permissions
from rest_framework.response import Response

from backend.models import OrderItemsModel, OrderModel, UserModel
from backend.serializers.user_serializers import (
    OrderDetailSerializer,
    OrderPositionSerializer,
    OrderSerializer,
    UserSerializer,
)


class UserProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request: HttpRequest):
        user = request.user
        serializer = self.serializer_class(user, context={"request": request})
        return Response(serializer.data)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()


class UserOrdersView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)


class UserOrderDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).prefetch_related("items__position")


class UserOrderPositionsView(generics.ListAPIView):
    permissions = (permissions.IsAuthenticated,)
    serializer_class = OrderPositionSerializer

    def get_queryset(self):
        return (
            OrderItemsModel.objects.filter(order=self.kwargs["pk"], order__user=self.request.user)
            .select_related("position__product", "position__shop")
            .prefetch_related("position__product__categories", "position__product_parameters__param")
        )
