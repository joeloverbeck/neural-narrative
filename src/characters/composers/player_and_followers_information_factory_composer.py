from src.base.validators import validate_non_empty_string
from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.combine_memories_algorithm_factory import (
    CombineMemoriesAlgorithmFactory,
)
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
    def __init__(
        self,
        playthrough_name: str,
        other_characters_role: str,
        other_characters_identifiers_strategy: OtherCharactersIdentifiersStrategy,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(other_characters_role, "other_characters_role")

        self._playthrough_name = playthrough_name
        self._other_characters_role = other_characters_role
        self._other_characters_identifiers_strategy = (
            other_characters_identifiers_strategy
        )

    def compose_factory(self) -> PlayerAndFollowersInformationFactory:
        player_data_for_prompt_factory = PlayerDataForPromptFactory(
            self._playthrough_name, CharacterFactory(self._playthrough_name)
        )

        combine_memories_algorithm_factory = CombineMemoriesAlgorithmFactory()

        party_data_for_prompt_factory = PartyDataForPromptFactory(
            self._playthrough_name,
            self._other_characters_role,
            self._other_characters_identifiers_strategy,
            player_data_for_prompt_factory,
            combine_memories_algorithm_factory,
        )

        return PlayerAndFollowersInformationFactory(party_data_for_prompt_factory)
