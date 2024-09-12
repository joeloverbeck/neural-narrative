from src.abstracts.command import Command
from src.characters.commands.store_generated_character_command import StoreGeneratedCharacterCommand
from src.constants import HERMES_405B
from src.maps.places_parameter import PlacesParameter
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.character_generation_tool_response_factory import CharacterGenerationToolResponseFactory
from src.prompting.factories.character_tool_response_data_extraction_factory import \
    CharacterToolResponseDataExtractionFactory


class GenerateCharacterCommand(Command):
    def __init__(self, playthrough_name: str, places_parameter: PlacesParameter,
                 tool_response_strategy: ProduceToolResponseStrategy):
        assert playthrough_name
        assert places_parameter
        assert tool_response_strategy

        self._playthrough_name = playthrough_name
        self._places_parameter = places_parameter
        self._tool_response_strategy = tool_response_strategy

    def execute(self) -> None:
        model = HERMES_405B

        llm_tool_response_product = CharacterGenerationToolResponseFactory(self._playthrough_name,
                                                                           self._places_parameter,
                                                                           self._tool_response_strategy).create_llm_response()

        if llm_tool_response_product.is_valid():
            # Extract character data using the function provided
            character_data = CharacterToolResponseDataExtractionFactory(
                llm_tool_response_product.get()).extract_data().get()

            StoreGeneratedCharacterCommand(self._playthrough_name, character_data).execute()
