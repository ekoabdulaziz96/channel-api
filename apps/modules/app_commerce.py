from django.conf import settings
from requests import request


class AppCommerceException(BaseException):
    pass

class AppCommerce():
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Api-Secret": settings.APP_COMMERCE_API_SECRET
        }
        self.base_url = settings.APP_COMMERCE_BASE_URL
    
    def _do_request(self):
        try:
            response = request(method=self.method, url=self.url, json=self.data, headers=self.headers)
            if response.status_code >= 400:
                raise AppCommerceException("error: ", response.content)
                
            print(response.json())

        except Exception as err:
            raise(err)

    def sync_channel(self, obj):
        self.method = "POST"
        self.url = self.base_url + "/api/v1/commerce/sync-channel/"
        self.data = {
            "store_slug": obj.store.slug,
            "name": obj.name,
            "slug": obj.slug,
            "types": obj.types
        }

        return self._do_request()

    def sync_order_open(self, data):
        self.method = "POST"
        self.url = self.base_url + "/api/v1/commerce/sync-order/open/"
        self.data = data
        return self._do_request()


app_commerce = AppCommerce()