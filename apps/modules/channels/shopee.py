from apps.modules.channels._abstracts import MarketplaceAbstract


class Shopee(MarketplaceAbstract):
    def sync_product(self):
        print("Shopee: process to sync product stock")

    def sync_order(self, status):
        print(f"Shopee: process to sync order with status {status}")

    def process_order(self):
        print("Shopee: process to process order")
