from apps.modules.channels._abstracts import MarketplaceAbstract


class Blibli(MarketplaceAbstract):
    def sync_product(self):
        print("Blibli: process to sync product stock")

    def sync_order(self):
        print("Blibli: process to sync order")

    def process_order(self):
        print("Blibli: process to process order")
