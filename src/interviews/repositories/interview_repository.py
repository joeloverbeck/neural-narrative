from typing import Optional

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    read_file,
    create_directories,
    create_empty_file_if_not_exists,
    write_file,
)
from src.filesystem.path_manager import PathManager


class InterviewRepository:
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

        self._path_manager = path_manager or PathManager()

        self._interview_path = self._path_manager.get_interview_path(
            playthrough_name, character_identifier, character_name
        )

        self._interview_file_path = self._path_manager.get_interview_file_path(
            playthrough_name, character_identifier, character_name
        )

    def get_interview(self) -> str:
        create_directories(self._interview_path)
        create_empty_file_if_not_exists(self._interview_file_path)

        return read_file(self._interview_file_path)

    def add_line(self, name: str, line: str):
        interview = self.get_interview()

        # Ensure the existing content ends with a newline
        if not interview.endswith("\n") and interview != "":
            interview += "\n"

        interview += f"{name}: {line}\n"

        write_file(self._interview_file_path, interview)
