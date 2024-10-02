import logging

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
from src.prompting.products.character_generation_guidelines_product import (
    CharacterGenerationGuidelinesProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class CharacterGenerationGuidelinesFactory(BaseToolResponseProvider):
    def __init__(
            self,
            playthrough_name: str,
            place_identifier: str,
            produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
            filesystem_manager: FilesystemManager = None,
            playthrough_manager: PlaythroughManager = None,
            map_manager: MapManager = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._map_manager = map_manager or MapManager(self._playthrough_name)

    def generate_character_generation_guidelines(
            self,
    ) -> CharacterGenerationGuidelinesProduct:

        world_name = self._playthrough_manager.get_world_template()
        world_description = self._map_manager.get_world_description()

        full_place_data = self._map_manager.get_place_full_data(self._place_identifier)

        # full_place_data should contain entries for 'region_data', 'area_data', etc.
        region_name = full_place_data["region_data"]["name"]
        region_description = full_place_data["region_data"]["description"]
        area_name = full_place_data["area_data"]["name"]
        area_description = full_place_data["area_data"]["description"]

        location_segment = ""

        if "location_data" in full_place_data and full_place_data["location_data"]:
            location_segment = f"Given the following description of a location of {area_name}, named {full_place_data["location_data"]["name"]}:"
            location_segment += (
                f"\n{full_place_data["location_data"]["description"]}\n----\n"
            )

        # Prepare the prompt
        prompt_template = self._read_prompt_file(
            CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE
        )
        formatted_prompt = self._format_prompt(
            prompt_template,
            world_name=world_name,
            world_description=world_description,
            region_name=region_name,
            region_description=region_description,
            area_name=area_name,
            area_description=area_description,
            location_segment=location_segment,
        )

        # Generate system content
        tool_data = self._read_tool_file(CHARACTER_GENERATION_GUIDELINES_TOOL_FILE)
        tool_instructions = self._read_tool_instructions()
        tool_prompt = self._generate_tool_prompt(tool_data, tool_instructions)
        system_content = self._generate_system_content(formatted_prompt, tool_prompt)

        # User content
        user_content = "Write about twenty entries that are guidelines for creating interesting characters based on the above combination of places. Be careful about following the provided instructions."

        # Produce tool response
        tool_response = self._produce_tool_response(system_content, user_content)

        # Extract arguments
        arguments = self._extract_arguments(tool_response)

        if not arguments.get("guidelines"):
            return CharacterGenerationGuidelinesProduct(
                [],
                is_valid=False,
                error="LLM returned empty or invalid list of guidelines.",
            )

        return CharacterGenerationGuidelinesProduct(
            arguments.get("guidelines"), is_valid=True
        )
