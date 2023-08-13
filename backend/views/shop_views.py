from rest_framework import generics

from backend.filters.shop_filters import ShopListFilterSet
from backend.models import ShopModel
from backend.serializers.shop_serializers import ShopDetailSerializer, ShopListSerializer


class ShopListView(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = ShopModel.objects.all()
    filterset_class = ShopListFilterSet


class ShopDetailView(generics.RetrieveAPIView):
    serializer_class = ShopDetailSerializer
    queryset = ShopModel.objects.all()
    lookup_field = "slug"
