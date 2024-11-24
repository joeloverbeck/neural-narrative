from typing import Optional

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.interviews.factories.move_to_next_base_question_command_factory import (
    MoveToNextBaseQuestionCommandFactory,
)
from src.interviews.repositories.ongoing_interview_repository import (
    OngoingInterviewRepository,
)
from src.interviews.repositories.questions_repository import QuestionsRepository


class DetermineNextInterviewQuestionCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
        move_to_next_base_question_command_factory: MoveToNextBaseQuestionCommandFactory,
        questions_repository: Optional[QuestionsRepository] = None,
        ongoing_interview_repository: Optional[OngoingInterviewRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(character_name, "character_name")

        self._move_to_next_base_question_command_factory = (
            move_to_next_base_question_command_factory
        )

        self._questions_repository = questions_repository or QuestionsRepository()
        self._ongoing_interview_repository = (
            ongoing_interview_repository
            or OngoingInterviewRepository(
                playthrough_name, character_identifier, character_name
            )
        )

    def execute(self) -> None:
        # If there was no set interview question in the repository, grab the first in the text file.
        if not self._ongoing_interview_repository.get_interview_question():
            interview_question = self._questions_repository.get_first()

            # Set it in the ongoing interview as the current interview question.
            self._ongoing_interview_repository.set_interview_question(
                interview_question
            )

            return

        # At this point, there is an interview question. It could be a base question (one existing in the questions file),
        # but it could also have been sent by the user.
        current_interview_question = (
            self._ongoing_interview_repository.get_interview_question()
        )

        if self._questions_repository.is_base_question(current_interview_question):
            # Just move to the next one for now.
            self._move_to_next_base_question_command_factory.create_command(
                current_interview_question
            ).execute()

            return

        # The current question isn't a base question.
        last_base_question = self._ongoing_interview_repository.get_last_base_question()

        if not last_base_question:
            raise ValueError(
                "The current interview question wasn't a base question, but there is no last base question set!"
            )

        self._move_to_next_base_question_command_factory.create_command(
            last_base_question
        ).execute()
