from pathlib import Path
from typing import Dict, Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.filesystem.file_operations import read_file
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider


class ConceptsManager:

    def __init__(
        self,
        playthrough_name: str,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._filesystem_manager = filesystem_manager or FilesystemManager()

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
                    Path(
                        self._filesystem_manager.get_file_path_to_facts(
                            self._playthrough_name
                        )
                    )
                )
            }
        )
        return prompt_data
