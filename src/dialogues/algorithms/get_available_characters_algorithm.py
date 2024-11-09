from typing import List, Optional

from src.base.validators import validate_list_of_str, validate_non_empty_string
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager


class GetAvailableCharactersAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        character_identifiers: List[str],
        characters_manager: Optional[CharactersManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_list_of_str(character_identifiers)

        self._character_identifiers = character_identifiers

        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )

    def do_algorithm(self) -> List[Character]:
        all_characters = (
            self._characters_manager.get_characters_at_current_place_plus_followers()
        )

        return [
            char
            for char in all_characters
            if char.identifier not in self._character_identifiers
        ]
