from rest_framework import generics

from backend.filters.product_filters import ProductListFilterSet
from backend.models import ProductModel, ProductShopModel
from backend.serializers.product_serializers import ProductListSerializer, ProductShopDetailListSerializer


class ProductListView(generics.ListAPIView):
    """
    Класс представления списка объектов из модели ProductModel
    Url: /products"""
    serializer_class = ProductListSerializer
    filterset_class = ProductListFilterSet

    def get_queryset(self):
        return (
            ProductModel.objects.filter(shops__status=True, productshopmodel__quantity__gt=0)
            .prefetch_related("categories", "shops")
            .distinct()
        )


class ProductShopDetailListView(generics.ListAPIView):
    """
     Класс детального представления списка объектов из модели ProductShopModel
     Url: /products/<slug:product>"""
    serializer_class = ProductShopDetailListSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "product"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return (
            ProductShopModel.objects.filter(product__slug=slug, shop__status=True, quantity__gt=0)
            .select_related("product", "shop")
            .prefetch_related("product_parameters__param", "product__categories")
        )
