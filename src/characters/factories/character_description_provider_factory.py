from src.characters.character import Character
from src.characters.providers.character_description_provider import CharacterDescriptionProvider
from src.prompting.factories.produce_tool_response_strategy_factory import ProduceToolResponseStrategyFactory


class CharacterDescriptionProviderFactory:

    def __init__(self, produce_tool_response_strategy_factory:
    ProduceToolResponseStrategyFactory):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory)

    def create_provider(self, character: Character):
        return CharacterDescriptionProvider(character, self.
                                            _produce_tool_response_strategy_factory)
