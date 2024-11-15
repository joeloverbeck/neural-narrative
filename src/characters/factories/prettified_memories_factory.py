from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy
from src.characters.characters_manager import CharactersManager
from src.characters.factories.combine_memories_algorithm_factory import (
    CombineMemoriesAlgorithmFactory,
)
from src.characters.factories.join_characters_memories_algorithm_factory import (
    JoinCharactersMemoriesAlgorithmFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)


class PrettifiedMemoriesFactory:

    def __init__(
        self,
        playthrough_name: str,
        other_characters_identifiers_strategy: OtherCharactersIdentifiersStrategy,
        combine_memories_algorithm_factory: CombineMemoriesAlgorithmFactory,
        join_characters_memories_algorithm_factory: JoinCharactersMemoriesAlgorithmFactory,
        player_data_for_prompt_factory: PlayerDataForPromptFactory,
        characters_manager: Optional[CharactersManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._other_characters_identifiers_strategy = (
            other_characters_identifiers_strategy
        )
        self._combine_memories_algorithm_factory = combine_memories_algorithm_factory
        self._join_characters_memories_algorithm_factory = (
            join_characters_memories_algorithm_factory
        )
        self._player_data_for_prompt_factory = player_data_for_prompt_factory

        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )

    def create_prettified_memories(self, query_text: str) -> str:
        validate_non_empty_string(query_text, "query_text")

        player_data_for_prompt = (
            self._player_data_for_prompt_factory.create_player_data_for_prompt(
                query_text
            )
        )

        # Retrieve the memories of characters other than the player.
        other_characters_ids = self._other_characters_identifiers_strategy.get_data()

        other_characters_data = self._characters_manager.get_characters(
            other_characters_ids
        )

        character_identifiers = [
            character.identifier for character in other_characters_data
        ]

        other_characters_memories = (
            self._join_characters_memories_algorithm_factory.create_algorithm(
                character_identifiers, query_text
            ).do_algorithm()
        )

        # Combine the memories of the player with those of other characters,
        # ensuring there are no duplicates.
        combined_memories = self._combine_memories_algorithm_factory.create_algorithm(
            player_data_for_prompt.get_player_memories(), other_characters_memories
        ).do_algorithm()

        # Join the list into a single string with each memory on a new line
        return "\n".join(combined_memories)
