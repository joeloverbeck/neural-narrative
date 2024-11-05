from typing import Dict, Optional

from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.templates_repository import TemplatesRepository


class GetPlaceFullDataAlgorithm:
    def __init__(
        self,
        place_identifier: str,
        place_manager_factory: PlaceManagerFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
        templates_repository: Optional[TemplatesRepository] = None,
    ):
        validate_non_empty_string(place_identifier, "place_identifier")

        self._place_identifier = place_identifier
        self._place_manager = place_manager_factory.create_place_manager()
        self._hierarchy_manager = hierarchy_manager_factory.create_hierarchy_manager()
        self._templates_repository = templates_repository or TemplatesRepository()

    def do_algorithm(self) -> Dict[str, Optional[Dict[str, str]]]:
        hierarchy = self._hierarchy_manager.get_place_hierarchy(self._place_identifier)

        result = {}
        for place_type in ["world", "region", "area", "location", "room"]:
            place_data = self._get_place_data(place_type, hierarchy.get(place_type))
            result[f"{place_type}_data"] = place_data

        return result

    def _get_place_data(self, place_type: str, place) -> Optional[Dict[str, str]]:
        if not place:
            return None

        template_name = self._place_manager.get_place_template(place)
        templates = self._templates_repository.load_templates(TemplateType(place_type))

        if template_name not in templates:
            raise KeyError(
                f"Template name '{template_name}' not present in the templates for '{place_type}'."
            )

        template_data = templates[template_name]
        if not template_data:
            raise ValueError(
                f"{place_type.capitalize()} template data is missing for '{template_name}'."
            )

        return {
            "name": template_name,
            "description": template_data.get("description"),
        }
