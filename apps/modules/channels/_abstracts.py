from abc import ABC, abstractmethod


class MarketplaceException(BaseException):
    pass


class MarketplaceAbstract(ABC):
    @abstractmethod
    def sync_product(self):
        raise MarketplaceException("not implemented yet!")

    @abstractmethod
    def sync_order(self):
        raise MarketplaceException("not implemented yet!")

    @abstractmethod
    def process_order(self):
        raise MarketplaceException("not implemented yet!")
