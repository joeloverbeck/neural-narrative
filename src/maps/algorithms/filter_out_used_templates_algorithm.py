from typing import Optional

from src.base.enums import TemplateType
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.templates_repository import TemplatesRepository


class FilterOutUsedTemplatesAlgorithm:
    def __init__(
        self,
        place_type: TemplateType,
        place_manager_factory: PlaceManagerFactory,
        templates_repository: Optional[TemplatesRepository] = None,
    ):
        self._place_type = place_type
        self._place_manager_factory = place_manager_factory

        self._templates_repository = templates_repository or TemplatesRepository()

    def do_algorithm(self) -> dict:
        available_templates = self._templates_repository.load_templates(
            self._place_type
        )

        # This is the only place where we can filter the templates, removing those already used for place_type.
        used_templates = (
            self._place_manager_factory.create_place_manager().get_places_of_type(
                self._place_type
            )
        )

        # Convert used_templates to a set for faster lookup
        used_templates_set = set(used_templates)

        # Filter out the used templates from available_templates
        return {
            template_name: template_data
            for template_name, template_data in available_templates.items()
            if template_name not in used_templates_set
        }
