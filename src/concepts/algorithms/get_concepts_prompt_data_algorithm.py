from typing import Dict

from src.base.validators import validate_non_empty_string
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider


class GetConceptsPromptDataAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: RelevantCharactersInformationFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._places_descriptions_factory = places_descriptions_factory
        self._player_and_followers_information_factory = (
            player_and_followers_information_factory
        )

    def do_algorithm(self) -> Dict[str, str]:
        prompt_data = {
            "places_descriptions": self._places_descriptions_factory.get_information()
        }
        prompt_data.update(
            {
                "player_and_followers_information": self._player_and_followers_information_factory.get_information()
            }
        )
        prompt_data.update(
            {"known_facts": self._format_known_facts_algorithm.do_algorithm()}
        )

        return prompt_data