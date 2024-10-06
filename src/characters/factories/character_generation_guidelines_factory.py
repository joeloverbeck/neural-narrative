import logging
from typing import Optional

from src.characters.products.character_generation_guidelines_product import (
    CharacterGenerationGuidelinesProduct,
)
from src.constants import (
    CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE,
    CHARACTER_GENERATION_GUIDELINES_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class CharacterGenerationGuidelinesFactory(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        place_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_manager: Optional[MapManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

        self._map_manager = map_manager or MapManager(self._playthrough_name)

    def get_prompt_file(self) -> str:
        return CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        world_name = self._playthrough_manager.get_world_template()
        world_description = self._map_manager.get_world_description()
        full_place_data = self._map_manager.get_place_full_data(self._place_identifier)

        region_name = full_place_data["region_data"]["name"]
        region_description = full_place_data["region_data"]["description"]
        area_name = full_place_data["area_data"]["name"]
        area_description = full_place_data["area_data"]["description"]

        location_segment = ""
        if "location_data" in full_place_data and full_place_data["location_data"]:
            location_name = full_place_data["location_data"]["name"]
            location_description = full_place_data["location_data"]["description"]
            location_segment = (
                f"Given the following description of a location of {area_name}, named {location_name}:\n"
                f"{location_description}\n----\n"
            )

        place_categories = self._map_manager.get_place_categories(
            self._map_manager.get_current_place_template(),
            self._map_manager.get_current_place_type(),
        )

        return {
            "world_name": world_name,
            "world_description": world_description,
            "region_name": region_name,
            "region_description": region_description,
            "area_name": area_name,
            "area_description": area_description,
            "location_segment": location_segment,
            "categories": ", ".join(place_categories),
        }

    def get_tool_file(self) -> str:
        return CHARACTER_GENERATION_GUIDELINES_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Write about twenty entries that are guidelines for creating interesting "
            "characters based on the above combination of places. Be careful about following "
            "the provided instructions."
        )

    def create_product(self, arguments: dict):
        if not arguments.get("guidelines"):
            return CharacterGenerationGuidelinesProduct(
                [],
                is_valid=False,
                error="LLM returned empty or invalid list of guidelines.",
            )
        return CharacterGenerationGuidelinesProduct(
            arguments.get("guidelines"), is_valid=True
        )
