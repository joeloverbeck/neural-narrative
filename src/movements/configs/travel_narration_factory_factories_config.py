from dataclasses import dataclass

from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


@dataclass
class TravelNarrationFactoryFactoriesConfig:
    produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    player_and_followers_information_factory: RelevantCharactersInformationFactory
    character_factory: CharacterFactory
    map_manager_factory: MapManagerFactory
