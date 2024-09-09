from django.db import models

from apps.bases.models import BaseModel, SafeDeleteModel
from apps.bases.utils import create_slug
from apps.modules.app_commerce import app_commerce


class Store(SafeDeleteModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    api_secret = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "app_channels_stores"

    def __str__(self):
        return self.slug


class Channel(SafeDeleteModel):
    NAME_CHOICES = (
        ("shopee", "Shopee"),
        ("tokopedia", "Tokopedia"),
        ("blibli", "Blibli"),
    )
    TYPE_CHOICES = (
        ("marketplace", "Marketplace"),
        ("shopify", "Shopify"),
        ("pos", "POS"),
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_channels")
    types = models.CharField(max_length=50, choices=TYPE_CHOICES)
    name = models.CharField(max_length=50, choices=NAME_CHOICES)
    slug = models.CharField(max_length=255, unique=True)
    account_id = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    api_secret = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "app_channels_channels"
        unique_together = ("store", "types", "name")

    def save(self, keep_deleted=False, **kwargs):
        if not self.slug:
            self.slug = create_slug(f"{self.types} {self.name} {self.account_name}", Store)

        app_commerce.sync_channel(self)

        return super().save(keep_deleted, **kwargs)


class StockUpdate(SafeDeleteModel):
    SYNC_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "failed"),
    )
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel_stock_updates")
    channel_product_id = models.CharField(max_length=255, default="")  # product_id from channel
    product_id = models.UUIDField()
    name = models.CharField(max_length=255, default="")
    stock = models.PositiveIntegerField(default=0)
    sync_status = models.CharField(max_length=50, choices=SYNC_STATUS_CHOICES)
    last_sync_at = models.DateTimeField(blank=True, null=True)
    err_message = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "app_channels_stock_updates"


class OrderUpdate(BaseModel):
    STATUS_CHOICES = [
        ("open", "open"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
        ("refund", "Refund"),
    ]
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel_order_updates")
    order_id = models.CharField(max_length=125, unique=True)  # from order number in specific channel
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    message = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "app_channels_order_updates"
