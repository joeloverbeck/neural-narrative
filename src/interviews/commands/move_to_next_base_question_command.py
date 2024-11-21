from typing import Optional

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.interviews.repositories.ongoing_interview_repository import (
    OngoingInterviewRepository,
)
from src.interviews.repositories.questions_repository import QuestionsRepository


class MoveToNextBaseQuestionCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
        interview_question: str,
        questions_repository: Optional[QuestionsRepository] = None,
        ongoing_interview_repository: Optional[OngoingInterviewRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(character_name, "character_name")
        validate_non_empty_string(interview_question, "interview_question")

        self._interview_question = interview_question

        self._questions_repository = questions_repository or QuestionsRepository()
        self._ongoing_interview_repository = (
            ongoing_interview_repository
            or OngoingInterviewRepository(
                playthrough_name, character_identifier, character_name
            )
        )

    def execute(self) -> None:
        # Must find the index of the current interview question in the questions file, then get the following one,
        # and set it as the current interview question.
        next_question = self._questions_repository.get_next_question(
            self._interview_question
        )

        self._ongoing_interview_repository.set_interview_question(next_question)
