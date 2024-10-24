import random
from typing import List, Dict, Optional

from src.base.enums import TemplateType
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.templates_repository import TemplatesRepository


class PlaceSelectionManager:

    def __init__(
        self,
        place_manager_factory: PlaceManagerFactory,
        template_repository: TemplatesRepository,
    ):
        self._place_manager_factory = place_manager_factory
        self._template_repository = template_repository

    def get_available_location_types(self, current_area_template: str) -> List[str]:
        place_categories = (
            self._place_manager_factory.create_place_manager().get_place_categories(
                current_area_template, TemplateType.AREA
            )
        )
        location_templates = self._template_repository.load_template(
            TemplateType.LOCATION
        )
        filtered_places = self.filter_places_by_categories(
            location_templates, place_categories
        )
        used_templates = (
            self._place_manager_factory.create_place_manager().get_places_of_type(
                TemplateType.LOCATION
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

    @staticmethod
    def filter_places_by_categories(
        place_templates: Dict,
        father_place_categories: List[str],
        location_type: Optional[str] = None,
    ) -> Dict:
        """Filter places whose categories match any of the father place's categories."""
        filtered_places = {}
        for name, data in place_templates.items():
            place_categories = data.get("categories", [])
            place_type = data.get("type", None)
            if not any(
                category in place_categories for category in father_place_categories
            ):
                continue
            if location_type and place_type != location_type:
                continue
            filtered_places[name] = data
        return filtered_places

    @staticmethod
    def select_random_place(matching_places: Dict) -> str:
        """Select a random place from the matching places."""
        if not matching_places:
            raise ValueError(
                "No matching places found. Consider generating places of the desired type."
            )
        return random.choice(list(matching_places.keys()))
