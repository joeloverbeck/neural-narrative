from typing import Optional

from src.base.constants import PLAYER_AND_FOLLOWERS_INFORMATION_BLOCK
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager


class PlayerAndFollowersInformationFactory:

    def __init__(
        self,
        party_data_for_prompt_factory: PartyDataForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._party_data_for_prompt_factory = party_data_for_prompt_factory
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def get_information(self) -> str:
        player_and_followers_information = self._filesystem_manager.read_file(
            PLAYER_AND_FOLLOWERS_INFORMATION_BLOCK
        )
        party_data_for_prompt = (
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )
        return player_and_followers_information.format(**party_data_for_prompt)
