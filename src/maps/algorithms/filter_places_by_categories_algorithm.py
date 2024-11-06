import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class FilterPlacesByCategoriesAlgorithm:
    def __init__(
        self,
        place_templates: Dict[str, Dict[str, Any]],
        father_place_categories: List[str],
        location_or_room_type: Optional[str] = None,
    ):
        self._place_templates = place_templates
        self._father_place_categories = father_place_categories
        self._location_or_room_type = location_or_room_type

    def do_algorithm(self) -> Dict[str, Dict[str, Any]]:
        """Filter places whose categories match any of the father place's categories."""
        filtered_places = {}

        for name, data in self._place_templates.items():
            place_categories = data.get("categories", [])
            location_or_room_type = data.get("type", None)

            if not any(
                category in place_categories
                for category in self._father_place_categories
            ):
                continue

            if (
                self._location_or_room_type
                and location_or_room_type != self._location_or_room_type
            ):
                continue

            filtered_places[name] = data

        return filtered_places
