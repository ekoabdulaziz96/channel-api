from rest_framework import serializers
from apps.app_channels.models import OrderUpdate, StockUpdate
from apps.bases.serializers import BaseModelSerializer, BaseSerializer, ChoiceDisplayField
from apps.modules.app_commerce import app_commerce
from apps.app_channels.tasks import sync_order_status_task


class OrderUpdateSerializer(BaseModelSerializer):
    order_id = serializers.CharField(required=True)
    status = ChoiceDisplayField(required=True, choices=OrderUpdate.STATUS_CHOICES)

    class Meta:
        model = OrderUpdate
        fields = ["order_id", "status"]

    def save(self, **kwargs):
        sync_order_status_task.delay(**self.validated_data)


class OrderItemSerializer(BaseSerializer):
    product_id = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        stock = StockUpdate.objects.filter(channel_product_id=data["product_id"]).first()
        data["product_id"] = str(stock.product_id)

        return data

class OrderShopeeSerializer(BaseSerializer):
    order_id = serializers.CharField(required=True)
    items = OrderItemSerializer(many=True)

    def save(self, **kwargs):
        # send order to commerce
        data = self.validated_data.copy()
        data["channel_slug"] = kwargs["channel"].slug
        app_commerce.sync_order_open(data)

        order, _ = OrderUpdate.objects.get_or_create(
            channel=kwargs["channel"], 
            order_id=self.validated_data["order_id"], 
            defaults={"status": "open"}
        )
        
        return OrderUpdateSerializer(order).data
