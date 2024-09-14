from typing import List

from src.maps.abstracts.abstract_factories import RandomPlaceTemplateBasedOnCategoriesFactory
from src.maps.abstracts.factory_products import PlaceTemplateProduct
from src.maps.map_manager import MapManager
from src.maps.products.concrete_place_template_product import ConcretePlaceTemplateProduct


class ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(RandomPlaceTemplateBasedOnCategoriesFactory):
    def __init__(self, map_manager: MapManager):
        if not map_manager:
            raise ValueError("map_manager should not be empty.")

        self._map_manager = map_manager

    def create_random_place_template_based_on_categories(self, place_templates: dict,
                                                         categories: List[str]) -> PlaceTemplateProduct:
        return ConcretePlaceTemplateProduct(
            self._map_manager.select_random_place(
                self._map_manager.filter_places_by_categories(place_templates, categories)),
            is_valid=True)
