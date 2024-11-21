from src.base.validators import validate_non_empty_string
from src.interviews.commands.move_to_next_base_question_command import (
    MoveToNextBaseQuestionCommand,
)


class MoveToNextBaseQuestionCommandFactory:
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(character_name, "character_name")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._character_name = character_name

    def create_command(self, interview_question: str) -> MoveToNextBaseQuestionCommand:
        validate_non_empty_string(interview_question, "interview_question")

        return MoveToNextBaseQuestionCommand(
            self._playthrough_name,
            self._character_identifier,
            self._character_name,
            interview_question,
        )
