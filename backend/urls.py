from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.views.product_views import ProductListView, ProductShopDetailListView
from backend.views.shop_views import (
    ShopDetailView,
    ShopListView,
    ShopOrderDetailsView,
    ShopOrderItemsView,
    ShopOrderView,
    ShopPriceFileUpdate,
    ShopPriceListView,
    ShopUpdateStatusView,
)
from backend.views.user_views import (
    CreateUserPasswordResetView,
    UserOrderDetailView,
    UserOrderPositionsView,
    UserOrdersView,
    UserPasswordUpdateView,
    UserProfileView,
    UserRegisterView,
)

urlpatterns = [
    # user
    path("users/profile/", UserProfileView.as_view(), name="profile"),
    path("users/profile/orders/", UserOrdersView.as_view(), name="orders"),
    path("users/profile/orders/<int:order>/", UserOrderDetailView.as_view(), name="order_detail"),
    path("users/profile/orders/<int:order>/items/", UserOrderPositionsView.as_view(), name="order_positions"),
    path("users/register/", UserRegisterView.as_view(), name="register"),
    path("users/token/", TokenObtainPairView.as_view(), name="token"),
    path("users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/password/reset", CreateUserPasswordResetView.as_view(), name="create_password_reset_token"),
    path("users/password/update/<str:user>/<uuid:token>/", UserPasswordUpdateView.as_view(), name="password_update"),
    # shop
    path("shops/", ShopListView.as_view(), name="shops"),
    path("shops/<slug:shop>/", ShopDetailView.as_view(), name="shop_details"),
    path("shops/<slug:shop>/orders/", ShopOrderView.as_view(), name="shop_orders"),
    path("shops/<slug:shop>/orders/<int:order>/", ShopOrderDetailsView.as_view(), name="shop_order_details"),
    path("shops/<slug:shop>/orders/<int:order>/items/", ShopOrderItemsView.as_view(), name="shop_order_items"),
    path("shops/<slug:shop>/products/", ShopPriceListView.as_view(), name="shop_price_list"),
    path("shops/<slug:shop>/status/", ShopUpdateStatusView.as_view(), name="shop_update_status"),
    path("shops/<slug:shop>/update/", ShopPriceFileUpdate.as_view(), name="shop_update_price_file"),
    # product
    path("products/", ProductListView.as_view(), name="products"),
    path("products/<slug:product>/", ProductShopDetailListView.as_view(), name="product_details_list"),
]
