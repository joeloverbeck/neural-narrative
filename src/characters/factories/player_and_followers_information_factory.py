from pathlib import Path

from src.base.constants import PLAYER_AND_FOLLOWERS_INFORMATION_BLOCK
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.filesystem.file_operations import read_file


class PlayerAndFollowersInformationFactory:

    def __init__(
        self,
        party_data_for_prompt_factory: PartyDataForPromptFactory,
    ):
        self._party_data_for_prompt_factory = party_data_for_prompt_factory

    def get_information(self) -> str:
        player_and_followers_information = read_file(
            Path(PLAYER_AND_FOLLOWERS_INFORMATION_BLOCK)
        )
        party_data_for_prompt = (
            self._party_data_for_prompt_factory.get_party_data_for_prompt()
        )

        return player_and_followers_information.format(**party_data_for_prompt)
