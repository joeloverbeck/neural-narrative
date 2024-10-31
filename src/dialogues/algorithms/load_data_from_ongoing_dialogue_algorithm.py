from typing import List, Optional, Dict, Any

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager


class LoadDataFromOngoingDialogueAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        dialogue_participants_identifiers: Optional[List[str]],
        purpose: Optional[str],
        has_ongoing_dialogue: bool,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._dialogue_participants_identifiers = dialogue_participants_identifiers
        self._purpose = purpose
        self._has_ongoing_dialogue = has_ongoing_dialogue

        self._path_manager = path_manager or PathManager()

    def do_algorithm(self) -> Dict[str, Any]:
        data = {}

        if self._has_ongoing_dialogue and (
            not self._dialogue_participants_identifiers or not self._purpose
        ):
            # We have an ongoing dialogue on file, but the session data has been lost.
            ongoing_dialogue_file = read_json_file(
                self._path_manager.get_ongoing_dialogue_path(self._playthrough_name)
            )

            if (
                not "participants" in ongoing_dialogue_file
                or not "purpose" in ongoing_dialogue_file
            ):
                raise ValueError(
                    f"Malformed ongoing dialogue file: {ongoing_dialogue_file}"
                )

            # At this point, the necessary data is present in the loaded ongoing dialogue file.
            if not self._dialogue_participants_identifiers:
                data["participants"] = ongoing_dialogue_file.get("participants")
            if not self._purpose:
                data["purpose"] = ongoing_dialogue_file.get("purpose")

        return data
