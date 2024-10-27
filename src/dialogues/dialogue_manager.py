import os.path
from typing import Optional, List

from src.base.validators import validate_non_empty_string
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager


class DialogueManager:

    def __init__(
        self,
        playthrough_name: str,
        characters_manager: Optional[CharactersManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name

        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._path_manager = path_manager or PathManager()

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

    def load_transcription(self) -> Transcription:
        ongoing_dialogue_path = self._path_manager.get_ongoing_dialogue_path(
            self._playthrough_name
        )

        transcription = Transcription()

        if os.path.exists(ongoing_dialogue_path):
            ongoing_dialogue_file = read_json_file(ongoing_dialogue_path)

            for speech_turn in ongoing_dialogue_file["transcription"]:
                transcription.add_line(speech_turn)

            return transcription

    def remove_ongoing_dialogue(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        file_path = self._path_manager.get_ongoing_dialogue_path(playthrough_name)

        if os.path.exists(file_path):
            os.remove(file_path)
