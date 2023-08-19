from django.http import HttpRequest
from rest_framework import generics, permissions
from rest_framework.response import Response

from backend.models import OrderModel, OrderPositionModel, UserModel
from backend.serializers.user_serializers import (OrderDetailSerializer, OrderListSerializer, OrderPositionSerializer,
                                                  UserSerializer)


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


class UserOrdersView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)


class UserOrderDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).prefetch_related('positions__position')


class UserOrderPositionsView(generics.ListAPIView):
    permissions = (permissions.IsAuthenticated,)
    serializer_class = OrderPositionSerializer

    def get_queryset(self):
        return OrderPositionModel.objects.filter(order=self.kwargs['pk'],
                                                 order__user=self.request.user) \
            .select_related('position__product', 'position__shop') \
            .prefetch_related('position__product__categories', 'position__product_parameters__param')
