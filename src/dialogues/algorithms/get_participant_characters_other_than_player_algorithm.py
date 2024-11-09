from typing import List, Optional

from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string, validate_list_of_str
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager


class GetParticipantCharactersOtherThanPlayerAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        dialogue_participants: List[str],
        playthrough_manager: Optional[PlaythroughManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_list_of_str(dialogue_participants)

        self._dialogue_participants = dialogue_participants

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )

    def do_algorithm(self) -> List[Character]:
        protagonist_identifier = self._playthrough_manager.get_player_identifier()

        # Participants excluding protagonist
        participant_identifiers = [
            identifier
            for identifier in self._dialogue_participants
            if identifier != protagonist_identifier
        ]

        # Get participant characters
        return self._characters_manager.get_characters(participant_identifiers)
