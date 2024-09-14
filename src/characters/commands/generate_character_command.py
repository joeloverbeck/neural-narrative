import logging

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.characters.commands.store_generated_character_command import StoreGeneratedCharacterCommand
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.images.commands.generate_character_image_command import GenerateCharacterImageCommand
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.prompting.abstracts.abstract_factories import UserContentForCharacterGenerationFactory
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.character_generation_tool_response_factory import CharacterGenerationToolResponseProvider
from src.prompting.factories.character_tool_response_data_extraction_factory import \
    CharacterToolResponseDataExtractionFactory
from src.requests.abstracts.abstract_factories import UrlContentFactory

logger = logging.getLogger(__name__)


class GenerateCharacterCommand(Command):
    def __init__(self, playthrough_name: str, places_parameter: PlacesTemplatesParameter,
                 tool_response_strategy: ProduceToolResponseStrategy,
                 user_content_for_character_generation_factory: UserContentForCharacterGenerationFactory,
                 generated_image_factory: GeneratedImageFactory,
                 url_content_factory: UrlContentFactory,
                 characters_manager: CharactersManager = None):
        assert playthrough_name
        assert places_parameter
        assert tool_response_strategy

        if not user_content_for_character_generation_factory:
            raise ValueError("user_content_for_character_generation_factory should not be empty.")
        if not generated_image_factory:
            raise ValueError("generated_image_factory should not be empty.")
        if not url_content_factory:
            raise ValueError("url_content_factory should not be empty.")

        self._playthrough_name = playthrough_name
        self._places_parameter = places_parameter
        self._tool_response_strategy = tool_response_strategy
        self._user_content_for_character_generation_factory = user_content_for_character_generation_factory
        self._generated_image_factory = generated_image_factory
        self._url_content_factory = url_content_factory
        self._characters_manager = characters_manager or CharactersManager(self._playthrough_name)

    def execute(self) -> None:
        llm_tool_response_product = CharacterGenerationToolResponseProvider(self._playthrough_name,
                                                                            self._places_parameter,
                                                                            self._tool_response_strategy,
                                                                            self._user_content_for_character_generation_factory).create_llm_response()

        if not llm_tool_response_product.is_valid():
            logger.error(f"The LLM was unable to generate a character: {llm_tool_response_product.get_error()}")
            return

        # Extract character data using the function provided
        character_data = CharacterToolResponseDataExtractionFactory(
            llm_tool_response_product.get()).extract_data().get()

        StoreGeneratedCharacterCommand(self._playthrough_name, character_data).execute()

        # Now that the character is stored, we need to retrieve the latest character identifier,
        # then use it to generate the character image
        GenerateCharacterImageCommand(self._playthrough_name,
                                      self._characters_manager.get_latest_character_identifier(),
                                      self._generated_image_factory, self._url_content_factory).execute()
