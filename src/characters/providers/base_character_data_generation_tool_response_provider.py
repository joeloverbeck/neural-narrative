import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    CHARACTER_GENERATION_INSTRUCTIONS_FILE,
)
from src.base.enums import TemplateType
from src.base.tools import capture_traceback
from src.characters.models.base_character_data import BaseCharacterData
from src.filesystem.file_operations import read_file, read_json_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
from src.maps.templates_repository import TemplatesRepository
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
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        user_content_for_character_generation_factory: UserContentForCharacterGenerationFactory,
        character_generation_instructions_formatter_factory: CharacterGenerationInstructionsFormatterFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        templates_repository: Optional[TemplatesRepository] = None,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._playthrough_name = playthrough_name
        self._user_content_for_character_generation_factory = (
            user_content_for_character_generation_factory
        )
        self._character_generation_instructions_formatter_factory = (
            character_generation_instructions_formatter_factory
        )

        self._templates_repository = templates_repository or TemplatesRepository()
        self._path_manager = path_manager or PathManager()

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
        playthrough_metadata = read_json_file(
            self._path_manager.get_playthrough_metadata_path(self._playthrough_name)
        )
        worlds_templates = self._templates_repository.load_templates(TemplateType.WORLD)
        regions_templates = self._templates_repository.load_templates(
            TemplateType.REGION
        )
        areas_templates = self._templates_repository.load_templates(TemplateType.AREA)
        locations_templates = self._templates_repository.load_templates(
            TemplateType.LOCATION
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
