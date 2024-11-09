import os
from typing import Optional, Dict, Any

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager


class OngoingDialogueRepository:

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
        return read_json_file(self._ongoing_dialogue_path)

    def dialogue_exists(self) -> bool:
        return os.path.exists(self._ongoing_dialogue_path)

    def validate_dialogue_is_not_malformed(self) -> None:
        ongoing_dialogue_file = self._load_ongoing_dialogue_data()

        if (
            not "participants" in ongoing_dialogue_file
            or not "purpose" in ongoing_dialogue_file
        ):
            raise ValueError(
                f"Malformed ongoing dialogue file: {ongoing_dialogue_file}"
            )

    def get_participants(self) -> Dict[str, Dict[str, str]]:
        return self._load_ongoing_dialogue_data().get("participants")

    def get_purpose(self) -> str:
        return self._load_ongoing_dialogue_data().get("purpose")
