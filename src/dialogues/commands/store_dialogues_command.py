import logging
from pathlib import Path
from typing import Optional

from src.base.abstracts.command import Command
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.file_operations import append_to_file, create_directories
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class StoreDialoguesCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        transcription: Transcription,
        playthrough_manager: Optional[PlaythroughManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._transcription = transcription

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._path_manager = path_manager or PathManager()

    def _store_dialogue_for_participant(
        self, participant: str, prettified_dialogue: str
    ):
        character = Character(self._playthrough_name, participant)

        # Ensure that the folder that will contain the character's dialogues exists.
        create_directories(
            self._path_manager.get_character_path(
                self._playthrough_name, character.identifier, character.name
            )
        )

        character_dialogues_path = self._path_manager.get_dialogues_path(
            self._playthrough_name,
            character_identifier=character.identifier,
            character_name=character.name,
        )
        append_to_file(Path(character_dialogues_path), prettified_dialogue)
        logger.info(f"Saved dialogue at '{character_dialogues_path}'.")

    def execute(self) -> None:
        if not self._transcription.is_transcription_sufficient():
            logger.error("Won't save an empty or insufficient dialogue.")
            return
        for participant in self._participants.get_participant_keys():
            self._store_dialogue_for_participant(
                participant, self._transcription.get_prettified_transcription()
            )
        self._playthrough_manager.add_to_adventure(
            self._transcription.get_prettified_transcription()
        )
