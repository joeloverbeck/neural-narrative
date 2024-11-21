import logging
from typing import Optional, Dict, Any, List

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    read_json_file,
    create_directories,
    create_empty_json_file_if_not_exists,
    write_json_file,
)
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class OngoingInterviewRepository:
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

        self._character_name = character_name

        self._path_manager = path_manager or PathManager()

        self._interview_path = self._path_manager.get_interview_path(
            playthrough_name, character_identifier, character_name
        )

        self._ongoing_interview_path = self._path_manager.get_ongoing_interview_path(
            playthrough_name, character_identifier, character_name
        )

    def _load_ongoing_interview(self) -> Dict[str, Any]:
        create_directories(self._interview_path)
        create_empty_json_file_if_not_exists(self._ongoing_interview_path)

        return read_json_file(self._ongoing_interview_path)

    def _save_ongoing_interview(self, ongoing_interview: Dict[str, Any]):
        write_json_file(self._ongoing_interview_path, ongoing_interview)

    def _add_message(self, message: Dict[str, str]):
        messages = self.get_messages()

        messages.append(message)

        ongoing_interview = self._load_ongoing_interview()

        ongoing_interview["messages"] = messages

        self._save_ongoing_interview(ongoing_interview)

    def get_interview_question(self) -> Optional[str]:
        ongoing_interview = self._load_ongoing_interview()

        return ongoing_interview.get("interview_question", None)

    def set_interview_question(self, interview_question: str):
        validate_non_empty_string(interview_question, "interview_question")

        ongoing_interview = self._load_ongoing_interview()

        ongoing_interview["interview_question"] = interview_question

        self._save_ongoing_interview(ongoing_interview)

    def get_messages(self) -> List[Dict[str, str]]:
        ongoing_interview = self._load_ongoing_interview()

        return ongoing_interview.get("messages", [])

    def add_interviewer_message(self, interview_question: str):
        validate_non_empty_string(interview_question, "interview_question")

        self._add_message({"name": "interviewer", "message": interview_question})

    def add_interviewee_message(self, interviewee_response: str):
        validate_non_empty_string(interviewee_response, "interviewee_response")

        self._add_message(
            {"name": self._character_name, "message": interviewee_response}
        )
