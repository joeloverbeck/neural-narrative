from src.maps.factories.get_place_facts_provider_factory import (
    GetPlaceFactsProviderFactory,
)
from src.maps.factories.place_facts_provider_factory import PlaceFactsProviderFactory
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms


class GetPlaceFactsProviderFactoryComposer:

    @staticmethod
    def compose_factory() -> GetPlaceFactsProviderFactory:
        place_facts_produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_place_facts()
            ).compose_factory()
        )

        place_facts_provider_factory = PlaceFactsProviderFactory(
            place_facts_produce_tool_response_strategy_factory
        )

        return GetPlaceFactsProviderFactory(place_facts_provider_factory)
