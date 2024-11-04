from typing import List, Optional

from src.base.constants import PARENT_TEMPLATE_TYPE
from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.place_selection_manager import PlaceSelectionManager
from src.maps.templates_repository import TemplatesRepository


class GetAvailablePlaceTypesAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        current_place_template: str,
        place_type: TemplateType,
        place_manager_factory: PlaceManagerFactory,
        place_selection_manager: PlaceSelectionManager,
        templates_repository: Optional[TemplatesRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(current_place_template, "current_place_template")

        if place_type != TemplateType.LOCATION and place_type != TemplateType.ROOM:
            raise TypeError(
                f"Places other than locations and rooms don't have types, but you requested types for place type '{place_type}'."
            )

        self._playthrough_name = playthrough_name
        self._current_place_template = current_place_template
        self._place_type = place_type
        self._place_manager_factory = place_manager_factory
        self._place_selection_manager = place_selection_manager

        self._templates_repository = templates_repository or TemplatesRepository()

    def do_algorithm(self) -> List[str]:
        parent_template_type = PARENT_TEMPLATE_TYPE.get(self._place_type)

        location_templates = self._templates_repository.load_templates(self._place_type)

        place_categories = (
            self._place_manager_factory.create_place_manager().get_place_categories(
                self._current_place_template, parent_template_type
            )
        )

        filtered_places = self._place_selection_manager.filter_places_by_categories(
            location_templates, place_categories
        )

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

        return list(
            set(
                data.get("type")
                for data in available_places.values()
                if data.get("type")
            )
        )
