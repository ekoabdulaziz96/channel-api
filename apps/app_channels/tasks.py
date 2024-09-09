from celery import shared_task
from django.utils import timezone

from apps.app_channels.models import OrderUpdate, StockUpdate
from apps.modules.channels._factories import channel_factory


@shared_task
def sync_stock_update_task(product_id, name, stock):
    stock_updates = StockUpdate.objects.filter(product_id=product_id).all()
    if not stock_updates:
        return "no stock to sync"

    for stock_update in stock_updates:
        stock_update.name = name
        stock_update.stock = stock
        stock_update.sync_status = "pending"

        sync_channel_stock_task.delay(stock_update.id)
        stock_update.save()

    return "success"


@shared_task
def sync_channel_stock_task(stock_id):
    stock_update = StockUpdate.objects.filter(id=stock_id).select_related("channel").first()

    channel_name = stock_update.channel.name
    channel_class = channel_factory.get_class(channel_name)
    channel_class().sync_product()

    stock_update.sync_status = "success"
    stock_update.last_sync_at = timezone.localtime()
    stock_update.save()


@shared_task
def sync_order_status_task(order_id, status):
    order = OrderUpdate.objects.filter(order_id=order_id).select_related("channel").first()
    channel_class = channel_factory.get_class(order.channel.name)
    channel_class().sync_order(status)

    order.status = status
    order.save()
