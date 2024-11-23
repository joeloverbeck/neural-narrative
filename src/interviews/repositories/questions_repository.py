import logging
from typing import Optional, List

from src.filesystem.file_operations import read_json_file
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class QuestionsRepository:

    def __init__(self, path_manager: Optional[PathManager] = None):
        self._path_manager = path_manager or PathManager()
        self._questions_path = self._path_manager.get_questions()

        # Load the JSON data
        data = read_json_file(self._questions_path)

        # Extract the questions (keys of the JSON object)
        self._questions = list(data.keys())

    def _get_questions(self) -> List[str]:
        # Return the list of questions
        return self._questions

    def get_first(self) -> str:
        # Return the first question
        return self._get_questions()[0]

    def is_base_question(self, interview_question: str) -> bool:
        # Check if the interview question is in the list of questions
        # Strip whitespace to ensure accurate comparison
        return interview_question.strip() in [q.strip() for q in self._get_questions()]

    def get_next_question(self, interview_question: str) -> Optional[str]:
        questions = self._get_questions()

        # Strip whitespace from the input question
        interview_question_stripped = interview_question.strip()
        # Create a list of stripped questions for comparison
        stripped_questions = [q.strip() for q in questions]

        try:
            # Find the index of the current question
            index = stripped_questions.index(interview_question_stripped)
            # Check if there is a next question
            if index + 1 < len(questions):
                return questions[index + 1]
            else:
                logging.info(
                    f"The question '{interview_question}' is the last question and has no following question."
                )
                return None
        except ValueError:
            # Raise an error if the question is not found
            raise ValueError(
                f"The question '{interview_question}' was not found in the JSON file."
            )
