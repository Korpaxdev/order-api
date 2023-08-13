from rest_framework import generics

from backend.models import ShopModel
from backend.serializers.shop_serializers import ShopDetailSerializer, ShopListSerializer


class ShopListView(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = ShopModel.objects.all()


class ShopDetailView(generics.RetrieveAPIView):
    serializer_class = ShopDetailSerializer
    queryset = ShopModel.objects.all()
    lookup_field = "slug"
