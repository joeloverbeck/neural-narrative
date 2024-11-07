import logging
from typing import List, Optional

from src.base.products.text_product import TextProduct
from src.maps.abstracts.abstract_factories import (
    RandomPlaceTemplateBasedOnCategoriesFactory,
)
from src.maps.factories.filter_places_by_categories_algorithm_factory import (
    FilterPlacesByCategoriesAlgorithmFactory,
)
from src.maps.place_selection_manager import PlaceSelectionManager

logger = logging.getLogger(__name__)


class ConcreteRandomPlaceTemplateBasedOnCategoriesFactory(
    RandomPlaceTemplateBasedOnCategoriesFactory
):

    def __init__(
        self,
        filter_places_by_categories_algorithm_factory: FilterPlacesByCategoriesAlgorithmFactory,
        place_selection_manager: PlaceSelectionManager,
        place_type: Optional[str] = None,
    ):
        self._filter_places_by_categories_algorithm_factory = (
            filter_places_by_categories_algorithm_factory
        )
        self._place_selection_manager = place_selection_manager
        self._place_type = place_type

    def create_place(self, place_templates: dict, categories: List[str]) -> TextProduct:
        if not categories:
            raise ValueError(
                "Attempted to create a random place, but failed to pass the categories."
            )

        filtered_places = (
            self._filter_places_by_categories_algorithm_factory.create_algorithm(
                place_templates, categories
            ).do_algorithm()
        )

        if not filtered_places:
            error_text = (
                f"No available templates for the selected type in this '{self._place_type}'."
                if self._place_type
                else "No available templates."
            )
            return TextProduct(
                None,
                is_valid=False,
                error=error_text,
            )

        random_place = self._place_selection_manager.select_random_place(
            filtered_places
        )

        return TextProduct(random_place, is_valid=True)
