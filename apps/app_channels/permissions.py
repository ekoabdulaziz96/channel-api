from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from apps.app_channels.models import Channel, Store


class IsAuthenticatedStore(BasePermission):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        api_secret = request.headers.get("Api-Secret", None)

        return Store.objects.filter(api_secret=api_secret).exists()


class IsAuthenticatedAppCommerce(BasePermission):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        api_secret = request.headers.get("Api-Secret", None)

        return api_secret == settings.APP_CHANNEL_API_SECRET


class IsAuthenticatedShopee(BasePermission):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        api_secret = request.headers.get("Api-Secret", None)
        channel = Channel.objects.filter(api_secret=api_secret).first()
        if not channel:
            return False
        return api_secret == channel.api_secret
