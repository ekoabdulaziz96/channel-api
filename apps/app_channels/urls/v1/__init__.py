from django.urls import path

from apps.app_channels.views import channels, orders

urlpatterns = [
    path("sync-store/", channels.StoreSync.as_view(), name="store-sync"),
    path("sync-stock/", channels.StockSync.as_view(), name="stock-sync"),
    path("<str:slug>/", channels.ChannelDetail.as_view(), name="channel-detail"),
    path("<str:slug>/stocks/", channels.StockList.as_view(), name="stock-list"),
    path("<str:slug>/orders/", orders.OrderList.as_view(), name="order-list"),
    path("sync-order/status/", orders.OrderStatusSync.as_view(), name="order-status-sync"),
]
