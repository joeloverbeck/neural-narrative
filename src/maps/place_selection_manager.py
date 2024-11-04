import random
from typing import List, Dict, Optional

from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.templates_repository import TemplatesRepository


class PlaceSelectionManager:

    def __init__(
        self,
        place_manager_factory: PlaceManagerFactory,
        template_repository: Optional[TemplatesRepository] = None,
    ):
        self._place_manager_factory = place_manager_factory

        self._template_repository = template_repository or TemplatesRepository()

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
