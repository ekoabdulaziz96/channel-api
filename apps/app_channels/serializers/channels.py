from rest_framework import serializers

from apps.app_channels.models import Channel, StockUpdate, Store
from apps.app_channels.tasks import sync_stock_update_task
from apps.bases.serializers import BaseModelSerializer, ChoiceDisplayField


class StoreSyncSerializer(BaseModelSerializer):
    slug = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    api_secret = serializers.CharField(required=True)

    class Meta:
        model = Store
        fields = ["slug", "name", "api_secret"]

    def save(self, **kwargs):
        slug = self.validated_data.pop("slug")
        store, created = Store.objects.get_or_create(slug=slug, defaults=self.validated_data)
        if not created:
            store.name = self.validated_data["name"]
            store.api_secret = self.validated_data["api_secret"]
            store.save()

        self.instance = store


class ChannelSerializer(BaseModelSerializer):
    store = StoreSyncSerializer()
    name = ChoiceDisplayField(choices=Channel.NAME_CHOICES)
    types = ChoiceDisplayField(choices=Channel.TYPE_CHOICES)

    class Meta:
        model = Channel
        fields = ["store", "slug", "name", "types", "account_id", "account_name", "api_key", "api_secret"]


class StockSyncSerializer(BaseModelSerializer):
    product_id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    stock = serializers.IntegerField(required=True)

    class Meta:
        model = StockUpdate
        fields = ["product_id", "name", "stock"]

    def process(self, **kwargs):
        sync_stock_update_task.delay(**self.validated_data)


class ChannelStockSerializer(BaseModelSerializer):
    sync_status = ChoiceDisplayField(choices=StockUpdate.SYNC_STATUS_CHOICES)

    class Meta:
        model = StockUpdate
        fields = ["channel_product_id", "product_id", "name", "stock", "sync_status", "last_sync_at", "err_message"]
