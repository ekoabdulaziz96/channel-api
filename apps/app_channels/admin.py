from django.contrib import admin

from apps.app_channels.models import (
    Channel,
    OrderUpdate,
    StockUpdate,
    Store,
)


class StoreAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "api_secret")
    search_fields = ("name",)
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "types", "account_name", "account_id", "display_store")
    readonly_fields = ("slug",)
    search_fields = ("name",)
    ordering = ["-created_at"]

    def display_store(self, obj):
        return obj.store

    display_store.short_description = "Store"


class StockUpdateAdmin(admin.ModelAdmin):
    list_display = ("product_id", "channel_product_id", "name", "stock", "sync_status", "display_channel")
    search_fields = ("channel__store__name", "channel__name", "channel__slug", "product_id", "channel_product_id")
    readonly_fields = ("sync_status", "last_sync_at", "err_message")
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def display_channel(self, obj):
        return obj.channel.slug

    display_channel.short_description = "Channel"


class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ("order_id", "display_store", "display_channel", "status", "message")
    search_fields = ("channel__store__name", "channel__name", "channel__slug", "order_id", "status")
    readonly_fields = ("order_id", "channel", "status", "message")
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def display_store(self, obj):
        return obj.channel.store

    def display_channel(self, obj):
        return obj.channel.slug

    display_store.short_description = "Store"
    display_channel.short_description = "Channel"

admin.site.register(Store, StoreAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(StockUpdate, StockUpdateAdmin)
admin.site.register(OrderUpdate, OrderUpdateAdmin)
