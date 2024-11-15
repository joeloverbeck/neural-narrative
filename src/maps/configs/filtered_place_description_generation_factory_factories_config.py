from dataclasses import dataclass

from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.weathers_manager import WeathersManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


@dataclass
class FilteredPlaceDescriptionGenerationFactoryFactoriesConfig:
    produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    character_information_provider_factory: CharacterInformationProviderFactory
    place_manager_factory: PlaceManagerFactory
    weathers_manager: WeathersManager
