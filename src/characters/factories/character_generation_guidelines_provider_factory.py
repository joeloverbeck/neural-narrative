from src.characters.factories.character_generation_guidelines_provider import (
    CharacterGenerationGuidelinesProvider,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class CharacterGenerationGuidelinesProviderFactory:
    def __init__(
            self,
            produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
            places_descriptions_provider: PlacesDescriptionsProvider,
            place_manager_factory: PlaceManagerFactory,
            map_manager_factory: MapManagerFactory,
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._places_descriptions_provider = places_descriptions_provider
        self._place_manager_factory = place_manager_factory
        self._map_manager_factory = map_manager_factory

    def create_provider(self) -> CharacterGenerationGuidelinesProvider:
        return CharacterGenerationGuidelinesProvider(
            self._produce_tool_response_strategy_factory,
            self._places_descriptions_provider,
            self._place_manager_factory,
            self._map_manager_factory,
        )
