from typing import Optional

from src.base.abstracts.command import Command
from src.interviews.repositories.interview_repository import InterviewRepository
from src.interviews.repositories.ongoing_interview_repository import (
    OngoingInterviewRepository,
)
from src.interviews.repositories.questions_repository import QuestionsRepository


class SkipInterviewQuestionCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
        interview_repository: Optional[InterviewRepository] = None,
        ongoing_interview_repository: Optional[OngoingInterviewRepository] = None,
        questions_repository: Optional[QuestionsRepository] = None,
    ):
        self._interview_repository = interview_repository or InterviewRepository(
            playthrough_name, character_identifier, character_name
        )
        self._ongoing_interview_repository = (
            ongoing_interview_repository
            or OngoingInterviewRepository(
                playthrough_name, character_identifier, character_name
            )
        )
        self._questions_repository = questions_repository or QuestionsRepository()

    def execute(self) -> None:
        # We must check that the latest entry in the interview is that of the interviewer.
        if not self._interview_repository.does_last_entry_belong_to_interviewer():
            raise ValueError(
                "The latest line in the interview didn't belong to the interviewer."
            )

        # We must also check if the last question in the messages of the ongoing interview belongs to the interviewer.
        if (
            not self._ongoing_interview_repository.does_last_entry_belong_to_interviewer()
        ):
            raise ValueError(
                "The latest message in the interview didn't belong to the interviewer."
            )

        # Must remove both previous questions.
        self._interview_repository.remove_latest_interviewer_question()
        self._ongoing_interview_repository.remove_latest_interviewer_question()

        current_interview_question = (
            self._ongoing_interview_repository.get_interview_question()
        )

        # Note: the current interview question may not be a base question.

        if self._questions_repository.is_base_question(current_interview_question):
            next_interview_question = self._questions_repository.get_next_question(
                current_interview_question
            )
        else:
            # The current question is a user question.
            last_base_question = (
                self._ongoing_interview_repository.get_last_base_question()
            )

            next_interview_question = self._questions_repository.get_next_question(
                last_base_question
            )

        self._ongoing_interview_repository.set_interview_question(
            next_interview_question
        )

        # Must add that new question to both the interview and the ongoing interview.
        self._interview_repository.add_line("Interviewer", next_interview_question)
        self._ongoing_interview_repository.add_interviewer_message(
            next_interview_question
        )
