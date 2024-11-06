from typing import Dict, Any, List, Optional

from src.maps.algorithms.filter_places_by_categories_algorithm import (
    FilterPlacesByCategoriesAlgorithm,
)


class FilterPlacesByCategoriesAlgorithmFactory:

    def __init__(self, location_or_room_type: Optional[str] = None):
        self._location_or_room_type = location_or_room_type

    def create_algorithm(
        self,
        place_templates: Dict[str, Dict[str, Any]],
        father_place_categories: List[str],
    ) -> FilterPlacesByCategoriesAlgorithm:
        return FilterPlacesByCategoriesAlgorithm(
            place_templates, father_place_categories, self._location_or_room_type
        )
