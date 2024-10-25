from src.base.validators import validate_non_empty_string
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_and_followers_information_factory import (
    PlayerAndFollowersInformationFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)


class PlayerAndFollowersInformationFactoryComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_factory(self) -> PlayerAndFollowersInformationFactory:
        player_data_for_prompt_factory = PlayerDataForPromptFactory(
            self._playthrough_name, CharacterFactory(self._playthrough_name)
        )
        party_data_for_prompt_factory = PartyDataForPromptFactory(
            self._playthrough_name, player_data_for_prompt_factory
        )
        return PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
