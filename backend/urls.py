from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.views.product_views import ProductListView, ProductShopDetailListView
from backend.views.shop_views import (ShopDetailView, ShopListView, ShopPriceFileUpdate, ShopPriceListView,
                                      ShopUpdateStatusView)
from backend.views.user_views import (UserOrderDetailView, UserOrderPositionsView, UserOrdersView, UserProfileView,
                                      UserRegisterView)

urlpatterns = [
    # user
    path("users/profile/", UserProfileView.as_view(), name="profile"),
    path("users/profile/orders", UserOrdersView.as_view(), name="orders"),
    path("users/profile/orders/<pk>", UserOrderDetailView.as_view(), name="order_detail"),
    path("users/profile/orders/<pk>/positions", UserOrderPositionsView.as_view(), name="order_positions"),
    path("users/register/", UserRegisterView.as_view(), name="register"),
    path("users/token/", TokenObtainPairView.as_view(), name="token"),
    path("users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # shop
    path("shops/", ShopListView.as_view(), name="shops"),
    path("shops/<slug>/", ShopDetailView.as_view(), name="shop_detail"),
    path("shops/<slug>/products/", ShopPriceListView.as_view(), name="shop_price_list"),
    path("shops/<slug>/status/", ShopUpdateStatusView.as_view(), name="shop_update_status"),
    path("shops/<slug>/update/", ShopPriceFileUpdate.as_view(), name="shop_update_price_file"),
    # product
    path("products/", ProductListView.as_view(), name="products"),
    path("products/<slug>/", ProductShopDetailListView.as_view(), name="product_details_list"),
]
