from typing import Protocol

from src.base.required_string import RequiredString
from src.requests.abstracts.factory_products import UrlContentProduct


class UrlContentFactory(Protocol):
    def get_url(self, url: RequiredString) -> UrlContentProduct:
        pass
