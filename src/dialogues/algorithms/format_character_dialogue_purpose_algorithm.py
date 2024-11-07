from typing import Optional

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import read_file_if_exists
from src.filesystem.path_manager import PathManager


class FormatCharacterDialoguePurposeAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(character_name, "character_name")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._character_name = character_name

        self._path_manager = path_manager or PathManager()

    def do_algorithm(self) -> str:
        purpose_path = self._path_manager.get_purpose_path(
            self._playthrough_name,
            self._character_identifier,
            self._character_name,
        )

        character_purpose = read_file_if_exists(purpose_path)

        return (
            f"{self._character_name}'s Dialogue Purpose: " + character_purpose
            if character_purpose
            else ""
        )
