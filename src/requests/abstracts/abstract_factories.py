from typing import Protocol
from src.requests.abstracts.factory_products import UrlContentProduct


class UrlContentFactory(Protocol):

    def get_url(self, url: str) -> UrlContentProduct:
        pass
