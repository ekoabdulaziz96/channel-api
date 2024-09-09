from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.app_channels import settings as app_settings
from apps.app_channels.models import Channel, StockUpdate
from apps.app_channels.paginations import StockPagination
from apps.app_channels.permissions import IsAuthenticatedAppCommerce, IsAuthenticatedStore
from apps.app_channels.serializers.channels import (
    ChannelSerializer,
    ChannelStockSerializer, 
    StoreSyncSerializer, 
    StockSyncSerializer,
)


class MixinChannel:
    def get_channel(self):
        channel = Channel.objects.filter(slug=self.kwargs["slug"]).first()
        if not channel:
            raise NotFound(app_settings.MSG_CHANNEL_NOT_FOUND)

        return channel
    

class StoreSync(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedAppCommerce]
    serializer_class = StoreSyncSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class StockSync(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedAppCommerce]
    serializer_class = StockSyncSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.process()

        return Response(data="sync stock still in progress.", status=status.HTTP_200_OK)
    

class ChannelDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()
    lookup_field = "slug"


class StockList(generics.ListAPIView, MixinChannel):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = ChannelStockSerializer
    pagination_class = StockPagination

    def get_queryset(self):
        channel = self.get_channel()
        return StockUpdate.objects.filter(channel=channel).all()