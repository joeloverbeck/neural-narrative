import logging
from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE,
    TOOL_INSTRUCTIONS_FOR_INSTRUCTOR_FILE,
)
from src.characters.models.character_guidelines import CharacterGuidelines
from src.characters.products.character_generation_guidelines_product import (
    CharacterGenerationGuidelinesProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.unparsed_string_produce_tool_response_strategy_factory import (
    UnparsedStringProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class CharacterGenerationGuidelinesProvider(BaseToolResponseProvider):

    def __init__(
        self,
        produce_tool_response_strategy_factory: UnparsedStringProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        place_manager_factory: PlaceManagerFactory,
        map_manager_factory: MapManagerFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)
        self._places_descriptions_factory = places_descriptions_factory
        self._place_manager_factory = place_manager_factory
        self._map_manager_factory = map_manager_factory

    def get_prompt_file(self) -> str:
        return CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        prompt_data = {
            "places_descriptions": self._places_descriptions_factory.get_information()
        }
        place_categories = self._place_manager_factory.create_place_manager().get_place_categories(
            self._map_manager_factory.create_map_manager().get_current_place_template(),
            self._place_manager_factory.create_place_manager().get_current_place_type(),
        )
        prompt_data.update(
            {"categories": ", ".join([category for category in place_categories])}
        )
        return prompt_data

    def _get_tool_data(self) -> dict:
        return CharacterGuidelines.model_json_schema()

    @staticmethod
    def _generate_tool_prompt(tool_data: dict, tool_instructions: str) -> str:
        return f"{tool_instructions} {tool_data}"

    def _read_tool_instructions(self) -> str:
        """Reads the tool instructions from the filesystem."""
        return self._filesystem_manager.read_file(TOOL_INSTRUCTIONS_FOR_INSTRUCTOR_FILE)

    def get_user_content(self) -> str:
        return "Write three entries that are guidelines for creating interesting characters based on the above combination of places. Follow the provided instructions."

    def create_product_from_base_model(self, base_model: BaseModel):
        return CharacterGenerationGuidelinesProduct(
            base_model.guidelines,
            is_valid=True,
        )
