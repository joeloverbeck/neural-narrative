import requests

from src.base.constants import REQUEST_OK
from src.requests.abstracts.abstract_factories import UrlContentFactory
from src.requests.abstracts.factory_products import UrlContentProduct
from src.requests.products.ConcreteUrlContentProduct import ConcreteUrlContentProduct


class ConcreteUrlContentFactory(UrlContentFactory):

    def get_url(self, url: str) -> UrlContentProduct:
        image_response = requests.get(url)

        if image_response.status_code == REQUEST_OK:
            return ConcreteUrlContentProduct(image_response.content, is_valid=True)
        else:
            return ConcreteUrlContentProduct(None, is_valid=False,
                                             error=f"Was unable to retrieve the contents of url '{url}': {image_response.status_code}")
