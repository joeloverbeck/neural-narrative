import logging
from typing import Optional

from src.abstracts.command import Command
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.playthrough_manager import PlaythroughManager

logger = logging.getLogger(__name__)


class StoreDialoguesCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        transcription: Transcription,
        filesystem_manager: Optional[FilesystemManager] = None,
        characters_manager: Optional[CharactersManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._transcription = transcription

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def _store_dialogue_for_participant(
        self, participant: str, prettified_dialogue: str
    ):
        character_dialogues_path = (
            self._filesystem_manager.get_file_path_to_character_dialogues(
                self._playthrough_name,
                character_identifier=participant,
                character_name=Character(self._playthrough_name, participant).name,
            )
        )

        self._filesystem_manager.append_to_file(
            character_dialogues_path, prettified_dialogue
        )

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
