from dataclasses import dataclass

from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


@dataclass
class LlmSpeechDataProviderFactoriesConfig:
    produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    places_descriptions_provider: PlacesDescriptionsProvider
    character_information_provider_factory: CharacterInformationProviderFactory
