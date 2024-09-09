from apps.modules.channels import shopee, tokopedia, blibli
from apps.modules.channels._abstracts import MarketplaceAbstract


class ChannelFactory():
    def __init__(self):
        self._set_factory()

    def _set_factory(self):
        self.channels = {
            "shopee": shopee.Shopee,
            "tokopedia": tokopedia.Tokopedia,
            "blibli": blibli.Blibli,
        }

    def get_class(self, name) -> MarketplaceAbstract:
        return self.channels.get(name)


channel_factory = ChannelFactory()