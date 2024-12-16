from typing import Optional

from pydantic import BaseModel

from src.base.products.text_product import TextProduct
from src.base.validators import validate_non_empty_string
from src.characters.factories.character_information_provider_factory import (
    CharacterInformationProviderFactory,
)
from src.filesystem.path_manager import PathManager
from src.interviews.repositories.interview_repository import InterviewRepository
from src.interviews.repositories.ongoing_interview_repository import (
    OngoingInterviewRepository,
)
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class IntervieweeResponseProvider(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        character_name: str,
        character_information_provider_factory: CharacterInformationProviderFactory,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
        interview_repository: Optional[InterviewRepository] = None,
        ongoing_interview_repository: Optional[OngoingInterviewRepository] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")
        validate_non_empty_string(character_name, "character_name")

        self._character_name = character_name
        self._character_information_provider_factory = (
            character_information_provider_factory
        )

        self._interview_repository = interview_repository or InterviewRepository(
            playthrough_name, character_identifier, character_name
        )
        self._ongoing_interview_repository = (
            ongoing_interview_repository
            or OngoingInterviewRepository(
                playthrough_name, character_identifier, character_name
            )
        )

    def get_prompt_file(self) -> str:
        return self._path_manager.get_interviewee_response_generation_prompt_path()

    def get_user_content(self) -> str:
        return f"Fully embody {self._character_name} to answer the interviewer's latest question."

    def create_product_from_base_model(self, response_model: BaseModel):
        interviewee_response = str(response_model.interviewee_response)

        return TextProduct(
            interviewee_response.replace("\n\n", " ").replace("\n", " "), is_valid=True
        )

    def get_prompt_kwargs(self) -> dict:
        interview = self._interview_repository.get_interview()

        character_information = (
            self._character_information_provider_factory.create_provider(
                interview, use_interview=False, use_memories=False
            ).get_information()
        )

        interview_question = self._ongoing_interview_repository.get_interview_question()

        return {
            "interview": interview,
            "name": self._character_name,
            "character_information": character_information,
            "interview_question": interview_question,
        }
