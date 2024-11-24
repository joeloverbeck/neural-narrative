from typing import Dict, Optional

from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.maps.algorithms.get_current_weather_identifier_algorithm import (
    GetCurrentWeatherIdentifierAlgorithm,
)
from src.maps.factories.get_place_facts_provider_factory import (
    GetPlaceFactsProviderFactory,
)
from src.maps.factories.get_place_full_data_algorithm_factory import (
    GetPlaceFullDataAlgorithmFactory,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.weathers_manager import WeathersManager


class PlaceDescriptionsForPromptFactory:

    def __init__(
        self,
        playthrough_name: str,
        get_place_full_data_algorithm_factory: GetPlaceFullDataAlgorithmFactory,
        get_current_weather_identifier_algorithm: GetCurrentWeatherIdentifierAlgorithm,
        get_place_facts_provider_factory: GetPlaceFactsProviderFactory,
        map_manager_factory: MapManagerFactory,
        weathers_manager: WeathersManager,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._get_place_full_data_algorithm_factory = (
            get_place_full_data_algorithm_factory
        )
        self._get_current_weather_identifier_algorithm = (
            get_current_weather_identifier_algorithm
        )
        self._get_place_facts_provider_factory = get_place_facts_provider_factory
        self._map_manager_factory = map_manager_factory
        self._weathers_manager = weathers_manager

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def _determine_location_description(
        self, place_full_data: Dict[str, Dict[str, str]]
    ) -> str:
        location_description = ""
        if (
            place_full_data["location_data"]
            and place_full_data["location_data"]["description"]
        ):
            location_facts = self._get_place_facts_provider_factory.create_provider(
                place_full_data["location_data"]["name"],
                place_full_data["location_data"]["description"],
                TemplateType.LOCATION,
            ).get_place_facts()

            return f"Location Facts:\n{str(location_facts)}"

        return location_description

    def _determine_room_description(
        self, place_full_data: Dict[str, Dict[str, str]]
    ) -> str:
        room_description = ""

        if place_full_data["room_data"] and place_full_data["room_data"]["description"]:
            room_facts = self._get_place_facts_provider_factory.create_provider(
                place_full_data["room_data"]["name"],
                place_full_data["room_data"]["description"],
                TemplateType.ROOM,
            ).get_place_facts()

            return f"Room Facts:\n{str(room_facts)}"

        return room_description

    def create_place_descriptions_for_prompt(self) -> Dict[str, str]:
        story_universe_template = (
            self._playthrough_manager.get_story_universe_template()
        )
        story_universe_description = (
            self._map_manager_factory.create_map_manager().get_story_universe_description()
        )

        story_universe_facts = self._get_place_facts_provider_factory.create_provider(
            story_universe_template,
            story_universe_description,
            TemplateType.STORY_UNIVERSE,
        ).get_place_facts()

        place_full_data = self._get_place_full_data_algorithm_factory.create_algorithm(
            self._playthrough_manager.get_current_place_identifier()
        ).do_algorithm()

        world_facts = self._get_place_facts_provider_factory.create_provider(
            place_full_data["world_data"]["name"],
            place_full_data["world_data"]["description"],
            TemplateType.WORLD,
        ).get_place_facts()

        region_facts = self._get_place_facts_provider_factory.create_provider(
            place_full_data["region_data"]["name"],
            place_full_data["region_data"]["description"],
            TemplateType.REGION,
        ).get_place_facts()

        area_facts = self._get_place_facts_provider_factory.create_provider(
            place_full_data["area_data"]["name"],
            place_full_data["area_data"]["description"],
            TemplateType.AREA,
        ).get_place_facts()

        return {
            "story_universe_description": story_universe_facts,
            "world_description": world_facts,
            "region_description": region_facts,
            "area_description": area_facts,
            "weather": self._weathers_manager.get_weather_description(
                self._get_current_weather_identifier_algorithm.do_algorithm()
            ),
            "location_description": self._determine_location_description(
                place_full_data
            ),
            "room_description": self._determine_room_description(place_full_data),
        }
