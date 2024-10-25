from typing import Protocol, List

from src.maps.abstracts.factory_products import (
    PlaceTemplateProduct,
    RandomTemplateTypeMapEntryCreationResult,
    CardinalConnectionCreationProduct,
)


class RandomPlaceTemplateBasedOnCategoriesFactory(Protocol):

    def create_place(
        self, place_templates: dict, categories: List[str]
    ) -> PlaceTemplateProduct:
        pass


class RandomTemplateTypeMapEntryProvider(Protocol):

    def create_map_entry(
        self,
    ) -> RandomTemplateTypeMapEntryCreationResult:
        pass


class CardinalConnectionCreationFactory(Protocol):

    def create_cardinal_connection(self) -> CardinalConnectionCreationProduct:
        pass
