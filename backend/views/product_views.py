from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from backend.filters.product_filters import ProductListFilterSet, ProductShopFilterSet
from backend.models import ProductModel, ProductShopModel
from backend.serializers.product_serializers import ProductListSerializer, ProductShopDetailListSerializer


@extend_schema_view(get=extend_schema(operation_id="products_list"))
class ProductListView(generics.ListAPIView):
    """
    Получение списка товаров
    """

    serializer_class = ProductListSerializer
    filterset_class = ProductListFilterSet

    def get_queryset(self):
        return (
            ProductModel.objects.filter(shops__status=True, productshopmodel__quantity__gt=0)
            .prefetch_related("categories", "shops")
            .distinct()
            .order_by("name")
        )


@extend_schema_view(get=extend_schema(operation_id="products_shops_detail_list"))
class ProductShopDetailListView(generics.ListAPIView):
    """
    Получение списка с информацией по товару {product} в магазинах
    """

    serializer_class = ProductShopDetailListSerializer
    filterset_class = ProductShopFilterSet
    lookup_field = "slug"
    lookup_url_kwarg = "product"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return (
            ProductShopModel.objects.filter(product__slug=slug, shop__status=True, quantity__gt=0)
            .select_related("product", "shop")
            .prefetch_related("product_parameters__param", "product__categories")
        )
