import random
from typing import Dict, Optional

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
    def select_random_place(matching_places: Dict) -> str:
        """Select a random place from the matching places."""
        if not matching_places:
            raise ValueError(
                "No matching places found. Consider generating places of the desired type."
            )
        return random.choice(list(matching_places.keys()))
