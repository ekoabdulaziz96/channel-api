from django.urls import path

from apps.app_channels.views import orders

urlpatterns = [
    path("webhook/order/shopee", orders.OrderShopee.as_view(), name="stock-list"),
]
