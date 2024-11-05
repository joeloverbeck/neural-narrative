from typing import Dict

from src.maps.algorithms.get_current_weather_identifier_algorithm import (
    GetCurrentWeatherIdentifierAlgorithm,
)
from src.maps.algorithms.get_place_full_data_algorithm import GetPlaceFullDataAlgorithm
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.weathers_manager import WeathersManager


class PlaceDescriptionsForPromptFactory:

    def __init__(
        self,
        get_place_full_data_algorithm: GetPlaceFullDataAlgorithm,
        get_current_weather_identifier_algorithm: GetCurrentWeatherIdentifierAlgorithm,
        map_manager_factory: MapManagerFactory,
        weathers_manager: WeathersManager,
    ):
        self._get_place_full_data_algorithm = get_place_full_data_algorithm
        self._get_current_weather_identifier_algorithm = (
            get_current_weather_identifier_algorithm
        )
        self._map_manager_factory = map_manager_factory
        self._weathers_manager = weathers_manager

    @staticmethod
    def _determine_location_description(
        place_full_data: Dict[str, Dict[str, str]]
    ) -> str:
        location_description = ""
        if (
            place_full_data["location_data"]
            and place_full_data["location_data"]["description"]
        ):
            location_description = (
                "Location Description: "
                + place_full_data["location_data"]["description"]
            )
        return location_description

    @staticmethod
    def _determine_room_description(place_full_data: Dict[str, Dict[str, str]]) -> str:
        room_description = ""

        if place_full_data["room_data"] and place_full_data["room_data"]["description"]:
            room_description = (
                "Room Description: " + place_full_data["room_data"]["description"]
            )

        return room_description

    def create_place_descriptions_for_prompt(self) -> Dict[str, str]:
        story_universe_description = (
            self._map_manager_factory.create_map_manager().get_story_universe_description()
        )
        place_full_data = self._get_place_full_data_algorithm.do_algorithm()

        return {
            "story_universe_description": story_universe_description,
            "world_description": place_full_data["world_data"]["description"],
            "region_description": place_full_data["region_data"]["description"],
            "area_description": place_full_data["area_data"]["description"],
            "weather": self._weathers_manager.get_weather_description(
                self._get_current_weather_identifier_algorithm.do_algorithm()
            ),
            "location_description": self._determine_location_description(
                place_full_data
            ),
            "room_description": self._determine_room_description(place_full_data),
        }
