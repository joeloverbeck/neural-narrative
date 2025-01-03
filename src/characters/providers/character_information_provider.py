from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.factories.character_factory import CharacterFactory
from src.characters.factories.retrieve_memories_algorithm_factory import (
    RetrieveMemoriesAlgorithmFactory,
)
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager
from src.interviews.repositories.interview_repository import InterviewRepository


class CharacterInformationProvider:

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        query_text: str,
        retrieve_memories_algorithm_factory: RetrieveMemoriesAlgorithmFactory,
        use_interview: bool,
        use_memories: bool,
        character_factory: CharacterFactory,
        path_manager: Optional[PathManager] = None,
        interview_repository: Optional[InterviewRepository] = None,
    ):
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(query_text, "query_text")

        self._character_identifier = character_identifier
        self._query_text = query_text
        self._retrieve_memories_algorithm_factory = retrieve_memories_algorithm_factory
        self._use_interview = use_interview
        self._use_memories = use_memories
        self._character_factory = character_factory

        self._character = self._character_factory.create_character(
            self._character_identifier
        )

        self._path_manager = path_manager or PathManager()
        self._interview_repository = interview_repository or InterviewRepository(
            playthrough_name, character_identifier, self._character.name
        )

    def _format_memories_output(self):
        memories = ""

        if self._use_memories:
            memories = "\n".join(
                self._retrieve_memories_algorithm_factory.create_algorithm(
                    self._character.identifier, self._query_text
                ).do_algorithm()
            )

        return memories

    def _format_interview_output(self, interview: str, memories: str):
        output = ""

        if self._use_memories:
            output = f"Relevant Memories:\n{memories}\n-----\n"

        output += f"Interview With {self._character.name}:\n{interview}"

        return output

    def get_information(self) -> str:
        # If the character has an interview, just return the interview.
        interview = self._interview_repository.get_interview()

        memories = self._format_memories_output()

        if self._use_interview and interview:
            return self._format_interview_output(interview, memories)

        character_information = read_file(
            self._path_manager.get_character_information_path()
        )

        character_information = character_information.format(
            **{
                "name": self._character.name,
                "description": self._character.description,
                "personality": self._character.personality,
                "profile": self._character.profile,
                "likes": self._character.likes,
                "dislikes": self._character.dislikes,
                "secrets": self._character.secrets,
                "speech_patterns": self._character.speech_patterns,
                "health": self._character.health,
                "equipment": self._character.equipment,
                "memories": memories,
            }
        )

        return character_information
