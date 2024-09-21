from src.characters.characters_manager import CharactersManager
from src.constants import (
    CHARACTER_GENERATOR_TOOL_FILE,
    CHARACTER_GENERATION_INSTRUCTIONS_FILE,
    TOOL_INSTRUCTIONS_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
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
from src.tools import generate_tool_prompt


class CharacterGenerationToolResponseProvider(ToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        places_parameter: PlacesTemplatesParameter,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        user_content_for_character_generation_factory: UserContentForCharacterGenerationFactory,
        filesystem_manager: FilesystemManager = None,
        characters_manager: CharactersManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._places_parameter = places_parameter
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._user_content_for_character_generation_factory = (
            user_content_for_character_generation_factory
        )

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def create_llm_response(self) -> LlmToolResponseProduct:
        try:
            templates = self._load_templates()

            location_name, location_description = self._get_location_details(
                templates["locations_templates"]
            )

            instructions = CharacterGenerationInstructionsFormatter(
                self._playthrough_name,
                location_name,
                location_description,
                templates,
                self._places_parameter,
            ).format()

            system_content = self._generate_system_content(instructions)

            user_content_product = (
                self._user_content_for_character_generation_factory.create_user_content_for_character_generation()
            )

            if not user_content_product.is_valid():
                return ConcreteLlmToolResponseProduct(
                    {},
                    is_valid=False,
                    error=(
                        "Was unable to create the user content for character generation: "
                        f"{user_content_product.get_error()}"
                    ),
                )

            response_data = self._produce_tool_response_strategy_factory.create_produce_tool_response_strategy().produce_tool_response(
                system_content, user_content_product.get()
            )

            return ConcreteLlmToolResponseProduct(response_data, is_valid=True)

        except Exception as e:
            return ConcreteLlmToolResponseProduct(
                {},
                is_valid=False,
                error=f"An error occurred while creating the LLM response: {str(e)}",
            )

    def _load_templates(self) -> dict:
        """Loads all necessary templates and metadata from the filesystem."""
        filesystem = self._filesystem_manager
        playthrough_metadata = filesystem.load_existing_or_new_json_file(
            filesystem.get_file_path_to_playthrough_metadata(self._playthrough_name)
        )
        worlds_templates = filesystem.load_existing_or_new_json_file(
            filesystem.get_file_path_to_worlds_template_file()
        )
        regions_templates = filesystem.load_existing_or_new_json_file(
            filesystem.get_file_path_to_regions_template_file()
        )
        areas_templates = filesystem.load_existing_or_new_json_file(
            filesystem.get_file_path_to_areas_template_file()
        )
        locations_templates = filesystem.load_existing_or_new_json_file(
            filesystem.get_file_path_to_locations_template_file()
        )
        character_generation_instructions = filesystem.read_file(
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
            location_name = (
                f"Here's the description of the location {location_template}:\n"
            )
            location_description = locations_templates[location_template]["description"]
            return location_name, location_description

        return "", ""

    def _generate_system_content(self, instructions: str) -> str:
        """Constructs the system content by combining the formatted instructions and the tool prompt."""
        tool_prompt = generate_tool_prompt(
            self._filesystem_manager.read_json_file(CHARACTER_GENERATOR_TOOL_FILE),
            self._filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE),
        )

        system_content = f"{instructions}\n\n{tool_prompt}"

        return system_content
