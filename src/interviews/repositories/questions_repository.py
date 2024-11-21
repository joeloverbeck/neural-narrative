import logging
from typing import Optional, List

from src.filesystem.file_operations import read_lines
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class QuestionsRepository:

    def __init__(self, path_manager: Optional[PathManager] = None):
        self._path_manager = path_manager or PathManager()

        self._questions_path = self._path_manager.get_questions()

    def _get_questions(self) -> List[str]:
        # Read lines and strip newline characters from each line
        return [line.rstrip("\n") for line in read_lines(self._questions_path)]

    def get_first(self) -> str:
        return self._get_questions()[0]  # No need to strip "\n" here

    def is_base_question(self, interview_question: str) -> bool:
        return interview_question in self._get_questions()

    def get_next_question(self, interview_question: str) -> Optional[str]:
        questions = self._get_questions()
        try:
            for index, line in enumerate(questions):
                if line == interview_question:
                    if index + 1 < len(questions):
                        return questions[index + 1]
                    else:
                        logging.info(
                            f"The line '{interview_question}' is the last line and has no following line."
                        )
                        raise None
            raise ValueError(
                f"The line '{interview_question}' was not found in the file."
            )
        except Exception as e:
            raise e
