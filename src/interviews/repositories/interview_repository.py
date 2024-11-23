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

    def does_last_entry_belong_to_interviewer(self) -> bool:
        interview = self.get_interview()
        lines = interview.rstrip("\n").split("\n")
        # Remove any empty lines at the end
        while lines and lines[-1] == "":
            lines.pop()
        if not lines:
            return False
        last_line = lines[-1]
        return last_line.startswith("Interviewer:")

    def remove_latest_interviewer_question(self):
        if not self.does_last_entry_belong_to_interviewer():
            raise Exception(
                "Cannot remove interviewer question: last line does not belong to the interviewer."
            )
        interview = self.get_interview()
        lines = interview.rstrip("\n").split("\n")
        # Remove any empty lines at the end
        while lines and lines[-1] == "":
            lines.pop()
        # Remove the last line (interviewer's question)
        lines.pop()
        new_interview = "\n".join(lines) + "\n" if lines else ""
        write_file(self._interview_file_path, new_interview)
