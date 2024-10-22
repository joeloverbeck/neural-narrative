from typing import Optional, List

from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.participants import Participants


class DialogueManager:

    def __init__(
        self, playthrough_name: str, characters_manager: CharactersManager = None
    ):
        self._playthrough_name = playthrough_name
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def gather_participants_data(
        self,
        player_identifier: Optional[str],
        participant_identifiers: List[str],
        participants: Participants,
    ):
        """Gathers the data of the participants into the Participants instance."""
        for participant_identifier in participant_identifiers:
            character = Character(self._playthrough_name, participant_identifier)
            participants.add_participant(
                character.identifier,
                character.name,
                character.description,
                character.personality,
                character.equipment,
                character.voice_model,
            )
        if player_identifier:
            character = Character(self._playthrough_name, player_identifier)
            participants.add_participant(
                character.identifier,
                character.name,
                character.description,
                character.personality,
                character.equipment,
                character.voice_model,
            )
