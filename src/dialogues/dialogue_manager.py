from typing import Optional, List

from src.characters.characters_manager import CharactersManager
from src.dialogues.participants import Participants


class DialogueManager:
    def __init__(
        self, playthrough_name: str, characters_manager: CharactersManager = None
    ):
        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )

    def gather_participants_data(
        self,
        player_identifier: Optional[str],
        participant_identifiers: List[str],
        participants: Participants,
    ):
        """Gathers the data of the participants into the Participants instance."""

        # Must now gather the data of the chosen participants.
        for participant_identifier in participant_identifiers:
            character_data = self._characters_manager.load_character_data(
                participant_identifier
            )

            participants.add_participant(
                character_data["identifier"],
                character_data["name"],
                character_data["description"],
                character_data["personality"],
                character_data["equipment"],
            )

        if player_identifier:
            # Also add the information of the player.
            character_data = self._characters_manager.load_character_data(
                player_identifier
            )

            participants.add_participant(
                character_data["identifier"],
                character_data["name"],
                character_data["description"],
                character_data["personality"],
                character_data["equipment"],
            )
