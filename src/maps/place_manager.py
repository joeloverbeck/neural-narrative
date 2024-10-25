import logging
from typing import Dict, List, Optional

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.maps.map_repository import MapRepository
from src.maps.templates_repository import TemplatesRepository

logger = logging.getLogger(__name__)


class PlaceManager:

    def __init__(
        self,
        playthrough_name: str,
        map_repository: MapRepository,
        template_repository: TemplatesRepository,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._map_repository = map_repository
        self._template_repository = template_repository
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def get_place(self, place_identifier: str) -> Dict:
        map_data = self._map_repository.load_map_data()
        place = map_data.get(place_identifier)
        if not place:
            raise ValueError(f"Place ID '{place_identifier}' not found.")
        return place

    @staticmethod
    def get_place_template(place: Dict) -> str:
        if not isinstance(place, Dict):
            raise TypeError(f"Expected place to be a Dict, but was '{type(place)}'.")
        template = place.get("place_template")
        if not template:
            raise ValueError(
                f"Place template not found for place ID '{place.get('id', 'unknown')}'."
            )
        return template

    def determine_place_type(self, place_identifier: str) -> TemplateType:
        place = self.get_place(place_identifier)
        place_type_str = place.get("type")
        try:
            return TemplateType(place_type_str)
        except ValueError:
            raise ValueError(
                f"Unknown place type '{place_type_str}' for place ID '{place_identifier}'."
            )

    def get_place_categories(
        self, place_template: str, place_type: TemplateType
    ) -> List[str]:
        templates = self._template_repository.load_template(place_type)
        place_data = templates.get(place_template)
        if not place_data:
            raise ValueError(f"'{place_template}' not found in {place_type} templates.")
        categories = place_data.get("categories")
        if not categories:
            raise ValueError(
                f"There were no categories for place template '{place_template}'."
            )
        return [category for category in categories]

    def get_places_of_type(self, place_type: TemplateType) -> List[str]:
        map_data = self._map_repository.load_map_data()
        return [
            place_data.get("place_template")
            for place_data in map_data.values()
            if place_data.get("type") == place_type.value
        ]

    def is_visited(self, place_identifier: str):
        map_file = self._map_repository.load_map_data()
        return map_file[place_identifier]["visited"]

    def set_as_visited(self, place_identifier: str):
        map_file = self._map_repository.load_map_data()
        map_file[place_identifier]["visited"] = True
        self._map_repository.save_map_data(map_file)

    def remove_character_from_place(
        self, character_identifier_to_remove: str, place_identifier: str
    ):
        place = self.get_place(place_identifier)

        place["characters"] = [
            character_id
            for character_id in place.get("characters", [])
            if character_id != character_identifier_to_remove
        ]

        map_file = self._map_repository.load_map_data()

        map_file[place_identifier] = place

        self._map_repository.save_map_data(map_file)

    def get_current_place_type(self) -> TemplateType:
        current_place_id = self._playthrough_manager.get_current_place_identifier()
        place = self.get_place(current_place_id)
        return TemplateType(place.get("type"))

    def add_location(self, place_identifier: str) -> None:
        if not self.get_current_place_type() == TemplateType.AREA:
            raise ValueError(
                "Attempted to add a location to a place that wasn't an area."
            )
        map_file = self._map_repository.load_map_data()
        if (
            place_identifier
            in map_file[self._playthrough_manager.get_current_place_identifier()][
                "locations"
            ]
        ):
            raise ValueError(
                f"Place identifier '{place_identifier}' already present in the locations of the current area."
            )
        map_file[self._playthrough_manager.get_current_place_identifier()][
            "locations"
        ].append(place_identifier)
        self._map_repository.save_map_data(map_file)

    def set_current_weather(self, weather_identifier: str) -> None:
        if not self.get_current_place_type() == TemplateType.AREA:
            raise ValueError(
                "Attempting to change the weather when the current place isn't an area!"
            )
        map_file = self._map_repository.load_map_data()
        map_file[self._playthrough_manager.get_current_place_identifier()][
            "weather_identifier"
        ] = weather_identifier
        self._map_repository.save_map_data(map_file)
