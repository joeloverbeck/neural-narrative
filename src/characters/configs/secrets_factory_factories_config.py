from dataclasses import dataclass

from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


@dataclass
class SecretsFactoryFactoriesConfig:
    produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    retrieve_memories_algorithm_factory: RetrieveMemoriesAlgorithmFactory
    character_factory: CharacterFactory
