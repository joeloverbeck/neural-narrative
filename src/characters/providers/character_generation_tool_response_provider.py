from typing import Optional

from src.characters.characters_manager import CharactersManager
from src.constants import (
    CHARACTER_GENERATOR_TOOL_FILE,
    CHARACTER_GENERATION_INSTRUCTIONS_FILE,
    WORLD_TEMPLATES_FILE,
    LOCATIONS_TEMPLATES_FILE,
    AREAS_TEMPLATES_FILE,
    REGIONS_TEMPLATES_FILE,
    VOICE_GENDERS,
    VOICE_AGES,
    VOICE_EMOTIONS,
    VOICE_TEMPOS,
    VOICE_VOLUMES,
    VOICE_TEXTURES,
    VOICE_TONES,
    VOICE_STYLES,
    VOICE_PERSONALITIES,
    VOICE_SPECIAL_EFFECTS,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.prompting.abstracts.abstract_factories import (
    ToolResponseProvider,
    UserContentForCharacterGenerationFactory,
)
from src.prompting.abstracts.factory_products import LlmToolResponseProduct
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.formatters.character_generation_instructions_formatter import (
    CharacterGenerationInstructionsFormatter,
)
from src.prompting.products.concrete_llm_tool_response_product import (
    ConcreteLlmToolResponseProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class CharacterGenerationToolResponseProvider(
    BaseToolResponseProvider, ToolResponseProvider
):
    def __init__(
        self,
        playthrough_name: str,
        places_parameter: PlacesTemplatesParameter,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        user_content_for_character_generation_factory: UserContentForCharacterGenerationFactory,
        places_description_factory: PlacesDescriptionsFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._places_parameter = places_parameter
        self._user_content_for_character_generation_factory = (
            user_content_for_character_generation_factory
        )
        self._places_description_factory = places_description_factory

        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def _read_and_format_tool_file(self, tool_file: str) -> dict:
        template_copy = self._filesystem_manager.load_existing_or_new_json_file(
            CHARACTER_GENERATOR_TOOL_FILE
        )

        try:
            template_copy["function"]["parameters"]["properties"]["voice_gender"][
                "enum"
            ] = VOICE_GENDERS
            template_copy["function"]["parameters"]["properties"]["voice_age"][
                "enum"
            ] = VOICE_AGES
            template_copy["function"]["parameters"]["properties"]["voice_emotion"][
                "enum"
            ] = VOICE_EMOTIONS
            template_copy["function"]["parameters"]["properties"]["voice_tempo"][
                "enum"
            ] = VOICE_TEMPOS
            template_copy["function"]["parameters"]["properties"]["voice_volume"][
                "enum"
            ] = VOICE_VOLUMES
            template_copy["function"]["parameters"]["properties"]["voice_texture"][
                "enum"
            ] = VOICE_TEXTURES
            template_copy["function"]["parameters"]["properties"]["voice_tone"][
                "enum"
            ] = VOICE_TONES
            template_copy["function"]["parameters"]["properties"]["voice_style"][
                "enum"
            ] = VOICE_STYLES
            template_copy["function"]["parameters"]["properties"]["voice_personality"][
                "enum"
            ] = VOICE_PERSONALITIES
            template_copy["function"]["parameters"]["properties"][
                "voice_special_effects"
            ]["enum"] = VOICE_SPECIAL_EFFECTS
        except Exception as e:
            raise ValueError(
                f"Was unable to format the character generator tool file: {e}"
            )

        return template_copy

    def _read_tool_file(self, tool_file: str) -> dict:
        return self._read_and_format_tool_file(tool_file)

    def get_formatted_prompt(self) -> str:
        templates = self._load_templates()

        instructions = CharacterGenerationInstructionsFormatter(
            self._playthrough_name,
            self._places_description_factory.get_information(),
            templates,
            self._places_parameter,
        ).format()

        return instructions

    def get_tool_file(self) -> str:
        return CHARACTER_GENERATOR_TOOL_FILE

    def get_user_content(self) -> str:
        user_content_product = (
            self._user_content_for_character_generation_factory.create_user_content_for_character_generation()
        )

        if not user_content_product.is_valid():
            raise ValueError(
                f"Unable to create user content for character generation: {user_content_product.get_error()}"
            )

        return user_content_product.get()

    def create_product(self, arguments: dict):
        return ConcreteLlmToolResponseProduct(arguments, is_valid=True)

    def create_llm_response(self) -> LlmToolResponseProduct:
        try:
            return self.generate_product()
        except Exception as e:
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
            WORLD_TEMPLATES_FILE
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
        character_generation_instructions = self._filesystem_manager.read_file(
            CHARACTER_GENERATION_INSTRUCTIONS_FILE
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
