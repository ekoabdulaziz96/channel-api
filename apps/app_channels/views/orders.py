from rest_framework import generics, status
from rest_framework.response import Response

from apps.app_channels.models import Channel, OrderUpdate
from apps.app_channels.permissions import IsAuthenticatedStore, IsAuthenticatedShopee, IsAuthenticatedAppCommerce
from apps.app_channels.paginations import OrderPagination
from apps.app_channels.serializers.orders import OrderUpdateSerializer, OrderShopeeSerializer
from apps.app_channels.views.channels import MixinChannel


class OrderList(generics.ListAPIView, MixinChannel):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = OrderUpdateSerializer
    pagination_class = OrderPagination
    ordering = ("-created_at",)

    def get_queryset(self):
        channel = self.get_channel()
        return OrderUpdate.objects.filter(channel=channel).all()
    

class OrderShopee(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedShopee]
    serializer_class = OrderShopeeSerializer

    def post(self, request, *args, **kwargs):
        api_secret = request.headers.get("Api-Secret", None)
        self.channel = Channel.objects.filter(api_secret=api_secret).first()
    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save(channel=self.channel)

        return Response(data, status=status.HTTP_200_OK)


class OrderStatusSync(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedAppCommerce]
    serializer_class = OrderUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
