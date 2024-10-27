from typing import Dict, Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider


class ConceptsManager:

    def __init__(
        self, playthrough_name: str, path_manager: Optional[PathManager] = None
    ):
        self._playthrough_name = playthrough_name

        self._path_manager = path_manager or PathManager()

    def get_prompt_data(
        self,
        places_descriptions_factory: PlacesDescriptionsProvider,
        player_and_followers_information_factory: PlayerAndFollowersInformationFactory,
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
            {
                "known_facts": read_file(
                    self._path_manager.get_facts_path(self._playthrough_name)
                )
            }
        )
        return prompt_data
