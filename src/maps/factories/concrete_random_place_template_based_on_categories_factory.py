from typing import List, Optional

from src.maps.abstracts.abstract_factories import (
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.abstracts.factory_products import PlaceTemplateProduct
from src.maps.place_selection_manager import PlaceSelectionManager
from src.maps.products.concrete_place_template_product import (
    ConcretePlaceTemplateProduct,
)


class ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
    RandomPlaceTemplateBasedOnCategoriesFactory
):

    def __init__(
        self,
        place_selection_manager: PlaceSelectionManager,
        location_type: Optional[str] = None,
    ):
        self._location_type = location_type
        self._place_selection_manager = place_selection_manager

    def create_random_place_template_based_on_categories(
        self, place_templates: dict, categories: List[str]
    ) -> PlaceTemplateProduct:
        if not categories:
            raise ValueError(
                "Attempted to create a random place, but failed to pass the categories."
            )
        filtered_places = self._place_selection_manager.filter_places_by_categories(
            place_templates, categories, self._location_type
        )
        random_place = self._place_selection_manager.select_random_place(
            filtered_places
        )
        if not random_place:
            return ConcretePlaceTemplateProduct(
                None,
                is_valid=False,
                error="No available templates for the selected type in this area.",
            )
        return ConcretePlaceTemplateProduct(random_place, is_valid=True)
