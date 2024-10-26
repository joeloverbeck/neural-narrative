import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    CHARACTER_GENERATION_INSTRUCTIONS_FILE,
    WORLDS_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
)
from src.base.tools import capture_traceback
from src.characters.characters_manager import CharactersManager
from src.characters.models.base_character_data import BaseCharacterData
from src.filesystem.file_operations import read_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.prompting.abstracts.abstract_factories import (
    ToolResponseProvider,
    UserContentForCharacterGenerationFactory,
    ProduceToolResponseStrategyFactory,
)
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.character_generation_instructions_formatter_factory import (
    CharacterGenerationInstructionsFormatterFactory,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class BaseCharacterDataGenerationToolResponseProvider(
    BaseToolResponseProvider, ToolResponseProvider
):

    def __init__(
        self,
        playthrough_name: str,
        places_parameter: PlacesTemplatesParameter,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        user_content_for_character_generation_factory: UserContentForCharacterGenerationFactory,
        character_generation_instructions_formatter_factory: CharacterGenerationInstructionsFormatterFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._places_parameter = places_parameter
        self._user_content_for_character_generation_factory = (
            user_content_for_character_generation_factory
        )
        self._character_generation_instructions_formatter_factory = (
            character_generation_instructions_formatter_factory
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def get_formatted_prompt(self) -> str:
        templates = self._load_templates()
        instructions = (
            self._character_generation_instructions_formatter_factory.create_formatter(
                templates
            ).format()
        )
        return instructions

    def get_user_content(self) -> str:
        user_content_product = (
            self._user_content_for_character_generation_factory.create_user_content_for_character_generation()
        )
        if not user_content_product.is_valid():
            raise ValueError(
                f"Unable to create user content for character generation: {user_content_product.get_error()}"
            )
        return user_content_product.get()

    def create_product_from_base_model(self, response_model: BaseModel):
        arguments = {
            "name": response_model.name,
            "description": response_model.description,
            "personality": response_model.personality,
            "profile": response_model.profile,
            "likes": response_model.likes,
            "dislikes": response_model.dislikes,
            "secrets": response_model.secrets,
            "health": response_model.health,
            "equipment": response_model.equipment,
            "voice_gender": response_model.voice_gender,
            "voice_age": response_model.voice_age,
            "voice_emotion": response_model.voice_emotion,
            "voice_tempo": response_model.voice_tempo,
            "voice_volume": response_model.voice_volume,
            "voice_texture": response_model.voice_texture,
            "voice_tone": response_model.voice_tone,
            "voice_style": response_model.voice_style,
            "voice_personality": response_model.voice_personality,
            "voice_special_effects": response_model.voice_special_effects,
        }
        return ConcreteLlmToolResponseProduct(arguments, is_valid=True)

    def create_llm_response(self) -> LlmToolResponseProduct:
        try:
            return self.generate_product(BaseCharacterData)
        except Exception as e:
            capture_traceback()
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"An error occurred while creating the LLM response: {e}",
            )

    def _load_templates(self) -> dict:
        """Loads all necessary templates and metadata from the filesystem."""
        playthrough_metadata = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_playthrough_metadata(
                self._playthrough_name
            )
        )
        worlds_templates = self._filesystem_manager.load_existing_or_new_json_file(
            WORLDS_TEMPLATES_FILE
        )
        regions_templates = self._filesystem_manager.load_existing_or_new_json_file(
            REGIONS_TEMPLATES_FILE
        )
        areas_templates = self._filesystem_manager.load_existing_or_new_json_file(
            AREAS_TEMPLATES_FILE
        )
        locations_templates = self._filesystem_manager.load_existing_or_new_json_file(
            LOCATIONS_TEMPLATES_FILE
        )
        character_generation_instructions = read_file(
            Path(CHARACTER_GENERATION_INSTRUCTIONS_FILE)
        )
        return {
            "playthrough_metadata": playthrough_metadata,
            "worlds_templates": worlds_templates,
            "regions_templates": regions_templates,
            "areas_templates": areas_templates,
            "locations_templates": locations_templates,
            "character_generation_instructions": character_generation_instructions,
        }

    def _get_location_details(self, locations_templates: dict) -> tuple:
        """Retrieves the location name and description if a location template is provided."""
        location_template = self._places_parameter.get_location_template()
        if location_template:
            location_name = f"Location: {location_template}:\n"
            location_description = locations_templates[location_template]["description"]
            return location_name, location_description
        return "", ""
