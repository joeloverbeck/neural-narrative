from typing import Optional

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.constants import CONCEPTS_GENERATION_TOOL_FILE, CONCEPTS_GENERATION_PROMPT_FILE
from src.events.products.concepts_product import ConceptsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ConceptsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        party_data_for_prompty_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_manager: Optional[MapManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._party_data_for_prompt_factory = party_data_for_prompty_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._map_manager = map_manager or MapManager(self._playthrough_name)

    def get_tool_file(self) -> str:
        return CONCEPTS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Generate five magnificent concepts for full stories. Follow the provided instructions."

    def create_product(self, arguments: dict):
        return ConceptsProduct(arguments.get("concepts"), is_valid=True)

    def get_prompt_file(self) -> Optional[str]:
        return CONCEPTS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        world_description = self._map_manager.get_world_description()

        place_data = self._map_manager.get_place_full_data(
            self._playthrough_manager.get_current_place_identifier()
        )

        region_description = place_data["region_data"]["description"]
        area_description = place_data["area_data"]["description"]

        location_description = ""

        if place_data["location_data"] and place_data["location_data"]["description"]:
            location_description = (
                "Location Description: " + place_data["location_data"]["description"]
            )

        prompt_data = {
            "world_description": world_description,
            "region_description": region_description,
            "area_description": area_description,
            "location_description": location_description,
        }

        prompt_data.update(
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )

        return prompt_data
