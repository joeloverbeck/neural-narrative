from typing import Dict

from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider


class ConceptsManager:

    def __init__(self, format_known_facts_algorithm: FormatKnownFactsAlgorithm):
        self._format_known_facts_algorithm = format_known_facts_algorithm

    def get_prompt_data(
        self,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: RelevantCharactersInformationFactory,
    ) -> Dict[str, str]:
        prompt_data = {
            "places_descriptions": places_descriptions_factory.get_information()
        }
        prompt_data.update(
            {
                "player_and_followers_information": player_and_followers_information_factory.get_information()
            }
        )
        prompt_data.update(
            {"known_facts": self._format_known_facts_algorithm.do_algorithm()}
        )

        return prompt_data
