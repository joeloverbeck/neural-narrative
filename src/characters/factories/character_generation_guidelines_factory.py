import logging
from typing import Optional

from src.base.constants import (
    CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE,
    CHARACTER_GENERATION_GUIDELINES_TOOL_FILE,
)
from src.base.playthrough_manager import PlaythroughManager
from src.characters.products.character_generation_guidelines_product import (
    CharacterGenerationGuidelinesProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.maps.map_manager import MapManager
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
        places_descriptions_factory: PlacesDescriptionsFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_manager: Optional[MapManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier
        self._places_descriptions_factory = places_descriptions_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

        self._map_manager = map_manager or MapManager(self._playthrough_name)

    def get_prompt_file(self) -> str:
        return CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        prompt_data = {
            "places_descriptions": self._places_descriptions_factory.get_information()
        }

        place_categories = self._map_manager.get_place_categories(
            self._map_manager.get_current_place_template(),
            self._map_manager.get_current_place_type(),
        )

        prompt_data.update(
            {
                "categories": ", ".join(place_categories),
            }
        )

        return prompt_data

    def get_tool_file(self) -> str:
        return CHARACTER_GENERATION_GUIDELINES_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Write three entries that are guidelines for creating interesting "
            "characters based on the above combination of places. Be careful about following "
            "the provided instructions."
        )

    def create_product(self, arguments: dict):
        return CharacterGenerationGuidelinesProduct(
            [
                arguments.get("guideline_1"),
                arguments.get("guideline_2"),
                arguments.get("guideline_3"),
            ],
            is_valid=True,
        )
