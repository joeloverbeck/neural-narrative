from typing import Protocol, List

from src.base.products.text_product import TextProduct
from src.maps.abstracts.factory_products import (
    RandomTemplateTypeMapEntryCreationResult,
    CardinalConnectionCreationProduct,
)


class RandomPlaceTemplateBasedOnCategoriesFactory(Protocol):

    def create_place(self, place_templates: dict, categories: List[str]) -> TextProduct:
        pass


class RandomTemplateTypeMapEntryProvider(Protocol):

    def create_map_entry(
        self,
    ) -> RandomTemplateTypeMapEntryCreationResult:
        pass


class CardinalConnectionCreationFactory(Protocol):

    def create_cardinal_connection(self) -> CardinalConnectionCreationProduct:
        pass
