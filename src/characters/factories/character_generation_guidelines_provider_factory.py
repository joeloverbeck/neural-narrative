from src.characters.factories.character_generation_guidelines_provider import (
    CharacterGenerationGuidelinesProvider,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class CharacterGenerationGuidelinesProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_provider: PlacesDescriptionsProvider,
        place_manager_factory: PlaceManagerFactory,
        map_manager_factory: MapManagerFactory,
    ):
        self._playthrough_name = playthrough_name
        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._places_descriptions_provider = places_descriptions_provider
        self._place_manager_factory = place_manager_factory
        self._map_manager_factory = map_manager_factory

    def create_provider(self) -> CharacterGenerationGuidelinesProvider:
        return CharacterGenerationGuidelinesProvider(
            self._playthrough_name,
            self._format_known_facts_algorithm,
            self._produce_tool_response_strategy_factory,
            self._places_descriptions_provider,
            self._place_manager_factory,
            self._map_manager_factory,
        )
