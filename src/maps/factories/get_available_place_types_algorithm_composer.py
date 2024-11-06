from typing import Optional

from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.factories.filter_places_by_categories_algorithm_factory import (
    FilterPlacesByCategoriesAlgorithmFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class GetAvailablePlaceTypesAlgorithmComposer:

    def __init__(
        self,
        playthrough_name: str,
        father_place_template: str,
        father_place_type: TemplateType,
        place_type: Optional[TemplateType] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(father_place_template, "father_place_template")

        self._playthrough_name = playthrough_name
        self._father_place_template = father_place_template
        self._father_place_type = father_place_type
        self._place_type = place_type

    def compose_algorithm(self) -> GetAvailablePlaceTypesAlgorithm:
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        filter_places_by_categories_algorithm_factory = (
            FilterPlacesByCategoriesAlgorithmFactory(self._place_type)
        )

        return GetAvailablePlaceTypesAlgorithm(
            self._playthrough_name,
            self._father_place_template,
            self._father_place_type,
            self._place_type,
            filter_places_by_categories_algorithm_factory,
            place_manager_factory,
        )
