from typing import Optional

from src.services.web_service import WebService


class ActionResolutionProduct:

    def __init__(
        self, narrative: str, outcome: str, is_valid: bool, error: Optional[str] = None
    ):
        if not narrative:
            raise ValueError("narrative can't be empty.")
        if not outcome:
            raise ValueError("outcome can't be empty.")
        self._narrative = narrative
        self._outcome = outcome
        self._is_valid = is_valid
        self._error = error
        self._narrative_voice_line_file_name = None
        self._outcome_voice_line_file_name = None

    def get_narrative(self) -> str:
        return self._narrative

    def get_outcome(self) -> str:
        return self._outcome

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error

    def set_narrative_voice_line_file_name(self, file_name) -> None:
        self._narrative_voice_line_file_name = file_name

    def set_outcome_voice_line_file_name(self, file_name) -> None:
        self._outcome_voice_line_file_name = file_name

    def get_narrative_voice_line_url(self):
        return WebService.get_file_url(
            "voice_lines", self._narrative_voice_line_file_name
        )

    def get_outcome_voice_line_url(self):
        return WebService.get_file_url(
            "voice_lines", self._outcome_voice_line_file_name
        )
