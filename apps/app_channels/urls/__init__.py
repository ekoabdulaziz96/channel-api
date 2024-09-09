from django.conf.urls import include
from django.urls import path

from apps.app_channels.urls import v1
from apps.app_channels.urls import webhooks

app_name = "app_channels"

urlpatterns = [
    path("api/v1/channels/", include(v1)),
    path("", include(webhooks)),
]
