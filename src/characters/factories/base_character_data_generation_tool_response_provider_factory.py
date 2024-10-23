from src.characters.providers.base_character_data_generation_tool_response_provider import (
    BaseCharacterDataGenerationToolResponseProvider,
)
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.prompting.abstracts.abstract_factories import (
    UserContentForCharacterGenerationFactory,
    ProduceToolResponseStrategyFactory,
)
from src.prompting.factories.character_generation_instructions_formatter_factory import (
    CharacterGenerationInstructionsFormatterFactory,
)


class BaseCharacterDataGenerationToolResponseProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        user_content_for_character_generation_factory: UserContentForCharacterGenerationFactory,
        character_generation_instructions_formatter_factory: CharacterGenerationInstructionsFormatterFactory,
    ):
        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._user_content_for_character_generation_factory = (
            user_content_for_character_generation_factory
        )
        self._character_generation_instructions_formatter_factory = (
            character_generation_instructions_formatter_factory
        )

    def create_response_provider(
        self, places_templates_parameter: PlacesTemplatesParameter
    ):
        return BaseCharacterDataGenerationToolResponseProvider(
            self._playthrough_name,
            places_templates_parameter,
            self._produce_tool_response_strategy_factory,
            self._user_content_for_character_generation_factory,
            self._character_generation_instructions_formatter_factory,
        )
