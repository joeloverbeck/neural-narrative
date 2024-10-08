from src.characters.providers.character_generation_tool_response_provider import (
    CharacterGenerationToolResponseProvider,
)
from src.maps.places_templates_parameter import PlacesTemplatesParameter
from src.prompting.abstracts.abstract_factories import (
    UserContentForCharacterGenerationFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class CharacterGenerationToolResponseProviderFactory:
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        user_content_for_character_generation_factory: UserContentForCharacterGenerationFactory,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._user_content_for_character_generation_factory = (
            user_content_for_character_generation_factory
        )

    def create_response_provider(
        self, places_templates_parameter: PlacesTemplatesParameter
    ):
        return CharacterGenerationToolResponseProvider(
            self._playthrough_name,
            places_templates_parameter,
            self._produce_tool_response_strategy_factory,
            self._user_content_for_character_generation_factory,
        )
