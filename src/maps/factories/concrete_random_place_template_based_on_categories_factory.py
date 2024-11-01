from typing import List, Optional

from src.base.products.text_product import TextProduct
from src.maps.abstracts.abstract_factories import (
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.place_selection_manager import PlaceSelectionManager


class ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
    RandomPlaceTemplateBasedOnCategoriesFactory
):

    def __init__(
        self,
        place_selection_manager: PlaceSelectionManager,
        location_type: Optional[str] = None,
    ):
        if isinstance(place_selection_manager, str):
            raise TypeError("place_selection_manager shouldn't be a string.")

        self._place_selection_manager = place_selection_manager
        self._location_type = location_type

    def create_place(self, place_templates: dict, categories: List[str]) -> TextProduct:
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
            return TextProduct(
                None,
                is_valid=False,
                error="No available templates for the selected type in this area.",
            )
        return TextProduct(random_place, is_valid=True)
