from src.base.validators import validate_non_empty_string
from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.combine_memories_algorithm_factory import (
    CombineMemoriesAlgorithmFactory,
)
from src.characters.factories.party_data_for_prompt_factory import (
    PartyDataForPromptFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.characters.factories.prettified_memories_factory import (
    PrettifiedMemoriesFactory,
)
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)


class RelevantCharactersInformationFactoryComposer:
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

    def compose_factory(self) -> RelevantCharactersInformationFactory:
        player_data_for_prompt_factory = PlayerDataForPromptFactory(
            self._playthrough_name, CharacterFactory(self._playthrough_name)
        )

        combine_memories_algorithm_factory = CombineMemoriesAlgorithmFactory()

        prettified_memories_factory = PrettifiedMemoriesFactory(
            self._playthrough_name,
            self._other_characters_identifiers_strategy,
            combine_memories_algorithm_factory,
            player_data_for_prompt_factory,
        )

        party_data_for_prompt_factory = PartyDataForPromptFactory(
            self._playthrough_name,
            self._other_characters_role,
            self._other_characters_identifiers_strategy,
            player_data_for_prompt_factory,
            prettified_memories_factory,
        )

        return RelevantCharactersInformationFactory(party_data_for_prompt_factory)
