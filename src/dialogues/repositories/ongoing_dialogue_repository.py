import logging
import os
from enum import Enum
from typing import Optional, Dict, Any, List

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    read_json_file,
    create_empty_json_file_if_not_exists,
    write_json_file,
    remove_file,
)
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class OngoingDialogueRepository:
    class OngoingDialogueEntryType(Enum):
        MESSAGES = "messages"
        PARTICIPANTS = "participants"
        PURPOSE = "purpose"
        TRANSCRIPTION = "transcription"

    def __init__(
        self, playthrough_name: str, path_manager: Optional[PathManager] = None
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

        self._path_manager = path_manager or PathManager()

        self._ongoing_dialogue_path = self._path_manager.get_ongoing_dialogue_path(
            self._playthrough_name
        )

    def _load_ongoing_dialogue_data(self) -> Dict[str, Any]:
        create_empty_json_file_if_not_exists(self._ongoing_dialogue_path)

        return read_json_file(self._ongoing_dialogue_path)

    def _save_ongoing_dialogue_data(
        self, ongoing_dialogue_data: Dict[str, Any]
    ) -> None:
        write_json_file(self._ongoing_dialogue_path, ongoing_dialogue_data)

    def dialogue_exists(self) -> bool:
        return os.path.exists(self._ongoing_dialogue_path)

    def _initialize_messages(self) -> None:
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        if not self.OngoingDialogueEntryType.MESSAGES.value in ongoing_dialogue_file:
            ongoing_dialogue_file[self.OngoingDialogueEntryType.MESSAGES.value] = []

            self._save_ongoing_dialogue_data(ongoing_dialogue_file)

    def get_messages(self) -> List[Dict[str, Any]]:
        return self._load_ongoing_dialogue_data().get(
            self.OngoingDialogueEntryType.MESSAGES.value, []
        )

    def add_messages(self, messages: List[Dict[str, Any]]):
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        self._initialize_messages()

        ongoing_dialogue_file[self.OngoingDialogueEntryType.MESSAGES.value].extend(
            messages
        )

        self._save_ongoing_dialogue_data(ongoing_dialogue_file)

    def validate_dialogue_is_not_malformed(self) -> None:
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        if (
            not self.OngoingDialogueEntryType.PARTICIPANTS.value
            in ongoing_dialogue_file
            or not self.OngoingDialogueEntryType.PURPOSE.value in ongoing_dialogue_file
        ):
            raise ValueError(
                f"Malformed ongoing dialogue file: {ongoing_dialogue_file}"
            )

    def has_participants(self) -> bool:
        return (
            self.OngoingDialogueEntryType.PARTICIPANTS.value
            in self._load_ongoing_dialogue_data()
        )

    def get_participants(self) -> Dict[str, Dict[str, str]]:
        return self._load_ongoing_dialogue_data().get(
            self.OngoingDialogueEntryType.PARTICIPANTS.value
        )

    def set_participants(self, participants: Dict[str, Dict[str, str]]) -> None:
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        ongoing_dialogue_file[self.OngoingDialogueEntryType.PARTICIPANTS.value] = (
            participants
        )

        self._save_ongoing_dialogue_data(ongoing_dialogue_file)

    def remove_participants(self, participants: List[str]) -> None:
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        for participant in participants:
            ongoing_dialogue_file[self.OngoingDialogueEntryType.PARTICIPANTS.value].pop(
                participant, None
            )

        self._save_ongoing_dialogue_data(ongoing_dialogue_file)

    def get_purpose(self) -> str:
        return self._load_ongoing_dialogue_data().get(
            self.OngoingDialogueEntryType.PURPOSE.value
        )

    def set_purpose(self, purpose: str) -> None:
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        ongoing_dialogue_file[self.OngoingDialogueEntryType.PURPOSE.value] = purpose

        self._save_ongoing_dialogue_data(ongoing_dialogue_file)

    def get_transcription(self) -> List[str]:
        return self._load_ongoing_dialogue_data().get(
            self.OngoingDialogueEntryType.TRANSCRIPTION.value
        )

    def set_transcription(self, transcription: List[str]) -> None:
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        ongoing_dialogue_file[self.OngoingDialogueEntryType.TRANSCRIPTION.value] = (
            transcription
        )

        self._save_ongoing_dialogue_data(ongoing_dialogue_file)

    def remove_dialogue(self) -> None:
        if self.dialogue_exists():
            remove_file(self._ongoing_dialogue_path)
