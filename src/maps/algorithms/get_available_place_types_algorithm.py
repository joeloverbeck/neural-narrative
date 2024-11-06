import logging
from typing import List, Optional

from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.factories.filter_places_by_categories_algorithm_factory import (
    FilterPlacesByCategoriesAlgorithmFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.templates_repository import TemplatesRepository

logger = logging.getLogger(__name__)


class GetAvailablePlaceTypesAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        father_place_template: str,
        father_place_type: TemplateType,
        place_type: TemplateType,
        filter_places_by_categories_algorithm_factory: FilterPlacesByCategoriesAlgorithmFactory,
        place_manager_factory: PlaceManagerFactory,
        templates_repository: Optional[TemplatesRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(father_place_template, "father_place_template")

        self._playthrough_name = playthrough_name
        self._father_place_template = father_place_template
        self._place_type = place_type
        self._father_place_type = father_place_type
        self._filter_places_by_categories_algorithm_factory = (
            filter_places_by_categories_algorithm_factory
        )
        self._place_manager_factory = place_manager_factory

        self._templates_repository = templates_repository or TemplatesRepository()

    def do_algorithm(self) -> List[str]:
        place_templates = self._templates_repository.load_templates(self._place_type)

        place_categories = (
            self._place_manager_factory.create_place_manager().get_place_categories(
                self._father_place_template, self._father_place_type
            )
        )

        filtered_places = (
            self._filter_places_by_categories_algorithm_factory.create_algorithm(
                place_templates, place_categories
            ).do_algorithm()
        )

        if not filtered_places:
            logger.warning(
                f"No filtered places for '{self._place_type}' given father place type '{self._father_place_type}'."
            )
            return []

        used_templates = (
            self._place_manager_factory.create_place_manager().get_places_of_type(
                self._place_type
            )
        )

        available_places = {
            identifier: data
            for identifier, data in filtered_places.items()
            if identifier not in used_templates
        }

        return list(set(identifier for identifier, data in available_places.items()))
