from typing import Dict, Optional

from src.base.playthrough_manager import PlaythroughManager
from src.base.playthrough_name import RequiredString
from src.maps.map_manager import MapManager
from src.maps.weathers_manager import WeathersManager


class PlaceDescriptionsForPromptFactory:
    def __init__(
        self,
        playthrough_name: str,
        map_manager: Optional[MapManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name

        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def create_place_descriptions_for_prompt(self) -> Dict[str, str]:
        world_description = self._map_manager.get_world_description()

        place_full_data = self._map_manager.get_place_full_data(
            self._playthrough_manager.get_current_place_identifier()
        )

        area = self._map_manager.get_current_area()

        region_description = place_full_data["region_data"]["description"]

        location_description = ""

        if (
            place_full_data["location_data"]
            and place_full_data["location_data"]["description"]
        ):
            location_description = (
                "Location Description: "
                + place_full_data["location_data"]["description"]
            )

        weathers_manager = WeathersManager(RequiredString(self._playthrough_name))

        return {
            "world_description": world_description,
            "region_description": region_description,
            "area_description": place_full_data["area_data"]["description"],
            "weather": weathers_manager.get_weather_description(
                weathers_manager.get_current_weather_identifier()
            ),
            "location_description": location_description,
        }
