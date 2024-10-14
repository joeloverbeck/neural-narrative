from typing import Dict, Optional

from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.places_descriptions_factory import PlacesDescriptionsFactory
from src.playthrough_name import PlaythroughName


class ConceptsManager:
    def __init__(
        self,
        playthrough_name: PlaythroughName,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._playthrough_name = playthrough_name

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def get_prompt_data(
        self,
        places_descriptions_factory: PlacesDescriptionsFactory,
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
                "known_facts": self._filesystem_manager.read_file(
                    self._filesystem_manager.get_file_path_to_facts(
                        self._playthrough_name.value
                    )
                )
            }
        )

        return prompt_data
