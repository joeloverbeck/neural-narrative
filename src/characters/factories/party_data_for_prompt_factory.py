from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy
from src.characters.character_memories import CharacterMemories
from src.characters.characters_manager import CharactersManager
from src.characters.factories.combine_memories_algorithm_factory import (
    CombineMemoriesAlgorithmFactory,
)
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)


class PartyDataForPromptFactory:

    def __init__(
        self,
        playthrough_name: str,
        other_characters_role: str,
        other_characters_identifiers_strategy: OtherCharactersIdentifiersStrategy,
        player_data_for_prompt_factory: PlayerDataForPromptFactory,
        combine_memories_algorithm_factory: CombineMemoriesAlgorithmFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        characters_manager: Optional[CharactersManager] = None,
        character_memories: Optional[CharacterMemories] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(other_characters_role, "other_characters_role")

        self._other_characters_role = other_characters_role
        self._other_characters_identifiers_strategy = (
            other_characters_identifiers_strategy
        )
        self._player_data_for_prompt_factory = player_data_for_prompt_factory
        self._combine_memories_algorithm_factory = combine_memories_algorithm_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )
        self._character_memories = character_memories or CharacterMemories(
            playthrough_name
        )

    def get_party_data_for_prompt(self) -> dict:
        player_data_for_prompt = (
            self._player_data_for_prompt_factory.create_player_data_for_prompt()
        )

        other_characters_ids = self._other_characters_identifiers_strategy.get_data()

        other_characters_data = self._characters_manager.get_characters(
            other_characters_ids
        )

        other_characters_info = self._characters_manager.get_characters_info(
            other_characters_data, self._other_characters_role
        )
        other_characters_memories = self._character_memories.join_characters_memories(
            other_characters_data
        )
        combined_memories = self._combine_memories_algorithm_factory.create_algorithm(
            player_data_for_prompt.get_player_memories(), other_characters_memories
        ).do_algorithm()

        data_for_prompt = player_data_for_prompt.get_player_data_for_prompt()

        # Join the list into a single string with each memory on a new line
        prettified_memories = "\n".join(combined_memories)

        data_for_prompt.update(
            {
                "other_characters_information": (
                    other_characters_info if other_characters_info else ""
                ),
                "combined_memories": prettified_memories,
            }
        )
        return data_for_prompt
