from typing import Dict, Optional

from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.repositories.facts_repository import FactsRepository
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider


class ConceptsManager:

    def __init__(
        self,
        playthrough_name: str,
        facts_repository: Optional[FactsRepository] = None,
    ):
        self._facts_repository = facts_repository or FactsRepository(playthrough_name)

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
        prompt_data.update({"known_facts": self._facts_repository.load_facts_file()})

        return prompt_data
