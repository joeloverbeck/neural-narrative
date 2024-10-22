from dataclasses import dataclass
from src.characters.factories.character_information_provider import CharacterInformationProvider
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.weathers_manager import WeathersManager
from src.prompting.factories.produce_tool_response_strategy_factory import ProduceToolResponseStrategyFactory


@dataclass
class FilteredPlaceDescriptionGenerationFactoryFactoriesConfig:
    produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    character_information_factory: CharacterInformationProvider
    place_manager_factory: PlaceManagerFactory
    map_manager_factory: MapManagerFactory
    weathers_manager: WeathersManager
