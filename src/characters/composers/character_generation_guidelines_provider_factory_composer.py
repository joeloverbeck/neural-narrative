from src.characters.factories.character_generation_guidelines_provider_factory import (
    CharacterGenerationGuidelinesProviderFactory,
)
from src.concepts.composers.format_known_facts_algorithm_composer import (
    FormatKnownFactsAlgorithmComposer,
)
from src.maps.composers.get_current_weather_identifier_algorithm_composer import (
    GetCurrentWeatherIdentifierAlgorithmComposer,
)
from src.maps.factories.get_place_full_data_algorithm_factory import (
    GetPlaceFullDataAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.maps.weathers_manager import WeathersManager
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms


class CharacterGenerationGuidelinesProviderFactoryComposer:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def compose_factory(self) -> CharacterGenerationGuidelinesProviderFactory:
        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_character_generation_guidelines(),
            ).compose_factory()
        )

        map_manager_factory = MapManagerFactory(self._playthrough_name)
        weathers_manager = WeathersManager()

        get_current_weather_identifier_algorithm = (
            GetCurrentWeatherIdentifierAlgorithmComposer(
                self._playthrough_name
            ).compose_algorithm()
        )

        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        hierarchy_manager_factory = HierarchyManagerFactory(self._playthrough_name)

        get_place_full_data_algorithm_factory = GetPlaceFullDataAlgorithmFactory(
            place_manager_factory,
            hierarchy_manager_factory,
        )

        place_descriptions_for_prompt_factory = PlaceDescriptionsForPromptFactory(
            self._playthrough_name,
            get_place_full_data_algorithm_factory,
            get_current_weather_identifier_algorithm,
            map_manager_factory,
            weathers_manager,
        )
        places_description_provider = PlacesDescriptionsProvider(
            place_descriptions_for_prompt_factory
        )
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        format_known_facts_algorithm = FormatKnownFactsAlgorithmComposer(
            self._playthrough_name
        ).compose_algorithm()

        return CharacterGenerationGuidelinesProviderFactory(
            self._playthrough_name,
            format_known_facts_algorithm,
            produce_tool_response_strategy_factory,
            places_description_provider,
            place_manager_factory,
            map_manager_factory,
        )
