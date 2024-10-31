from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy
from src.characters.characters_manager import CharactersManager
from src.characters.factories.player_data_for_prompt_factory import (
    PlayerDataForPromptFactory,
)
from src.characters.factories.prettified_memories_factory import (
    PrettifiedMemoriesFactory,
)


class PartyDataForPromptFactory:

    def __init__(
        self,
        playthrough_name: str,
        other_characters_role: str,
        other_characters_identifiers_strategy: OtherCharactersIdentifiersStrategy,
        player_data_for_prompt_factory: PlayerDataForPromptFactory,
        prettified_memories_factory: PrettifiedMemoriesFactory,
        characters_manager: Optional[CharactersManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(other_characters_role, "other_characters_role")

        self._other_characters_role = other_characters_role
        self._other_characters_identifiers_strategy = (
            other_characters_identifiers_strategy
        )
        self._player_data_for_prompt_factory = player_data_for_prompt_factory
        self._prettified_memories_factory = prettified_memories_factory

        self._characters_manager = characters_manager or CharactersManager(
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

        data_for_prompt = player_data_for_prompt.get_player_data_for_prompt()

        other_characters_info = self._characters_manager.get_characters_info(
            other_characters_data, self._other_characters_role
        )

        data_for_prompt.update(
            {
                "other_characters_information": (
                    other_characters_info if other_characters_info else ""
                ),
                "combined_memories": self._prettified_memories_factory.create_prettified_memories(),
            }
        )
        return data_for_prompt
