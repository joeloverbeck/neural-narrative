from typing import Dict, Any, List, Optional

from src.base.enums import TemplateType
from src.maps.algorithms.filter_places_by_categories_algorithm import (
    FilterPlacesByCategoriesAlgorithm,
)


class FilterPlacesByCategoriesAlgorithmFactory:

    def __init__(self, place_type: Optional[TemplateType] = None):
        self._place_type = place_type

    def create_algorithm(
        self,
        place_templates: Dict[str, Dict[str, Any]],
        father_place_categories: List[str],
    ) -> FilterPlacesByCategoriesAlgorithm:
        return FilterPlacesByCategoriesAlgorithm(
            place_templates, father_place_categories, self._place_type
        )
