from typing import Optional

from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager


class PlayerAndFollowersInformationFactory:

    def __init__(
        self,
        party_data_for_prompt_factory: PartyDataForPromptFactory,
        path_manager: Optional[PathManager] = None,
    ):
        self._party_data_for_prompt_factory = party_data_for_prompt_factory

        self._path_manager = path_manager or PathManager()

    def get_information(self) -> str:
        player_and_followers_information = read_file(
            self._path_manager.get_players_and_followers_information_path()
        )
        party_data_for_prompt = (
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )

        return player_and_followers_information.format(**party_data_for_prompt)
