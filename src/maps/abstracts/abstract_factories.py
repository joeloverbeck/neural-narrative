from abc import ABC, abstractmethod
from typing import Protocol, List

from src.base.required_string import RequiredString
from src.maps.abstracts.factory_products import (
    PlaceDataProduct,
    CurrentPlaceProduct,
    PlaceTemplateProduct,
    FullPlaceDataProduct,
    RandomTemplateTypeMapEntryCreationResult,
    CardinalConnectionCreationProduct,
)


class PlaceDataFactory(ABC):
    @abstractmethod
    def create_place_data(self) -> PlaceDataProduct:
        pass


class CurrentPlaceFactory(ABC):
    @abstractmethod
    def create_current_place(self) -> CurrentPlaceProduct:
        pass


class RandomPlaceTemplateBasedOnCategoriesFactory(Protocol):
    def create_random_place_template_based_on_categories(
            self, place_templates: dict, categories: List[RequiredString]
    ) -> PlaceTemplateProduct:
        pass


class FullPlaceDataFactory(Protocol):
    def create_full_place_data(self) -> FullPlaceDataProduct:
        pass


class RandomTemplateTypeMapEntryProvider(Protocol):
    def create_random_place_type_map_entry(
        self,
    ) -> RandomTemplateTypeMapEntryCreationResult:
        pass


class CardinalConnectionCreationFactory(Protocol):
    def create_cardinal_connection(self) -> CardinalConnectionCreationProduct:
        pass
