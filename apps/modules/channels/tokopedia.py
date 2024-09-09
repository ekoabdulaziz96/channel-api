from apps.modules.channels._abstracts import MarketplaceAbstract

class Tokopedia(MarketplaceAbstract):

    def sync_product(self):
        print("Tokopedia: process to sync product stock")

    def sync_order(self):
        print("Tokopedia: process to sync order")

    def process_order(self):
        print("Tokopedia: process to process order")