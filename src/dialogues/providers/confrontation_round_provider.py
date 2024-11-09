import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.base.products.text_product import TextProduct
from src.base.validators import validate_non_empty_string
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.dialogues.transcription import Transcription
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager

logger = logging.getLogger(__name__)


class ConfrontationRoundProvider(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        confrontation_context: str,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        relevant_characters_information_factory: RelevantCharactersInformationFactory,
        path_manager: Optional[PathManager] = None,
        time_manager: Optional[TimeManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(confrontation_context, "confrontation_context")

        self._playthrough_name = playthrough_name
        self._confrontation_context = confrontation_context
        self._transcription = transcription
        self._local_information_factory = local_information_factory
        self._relevant_characters_information_factory = (
            relevant_characters_information_factory
        )

        self._time_manager = time_manager or TimeManager(self._playthrough_name)

    def get_prompt_file(self) -> Path:
        return self._path_manager.get_confrontation_round_generation_prompt_path()

    def get_user_content(self) -> str:
        return f"Context of confrontation: {self._confrontation_context}\nWrite a compelling narrative that captures this intense moment of confrontation, reflecting both the actions and immediate consequences, while advancing the story in a meaningful way. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        # Log chain of thought.
        logger.info(
            "Confrontation round reasoning: %s",
            response_model.confrontation_round.chain_of_thought,
        )

        return TextProduct(response_model.confrontation_round.narration, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        facts_file = read_file(
            self._path_manager.get_facts_path(self._playthrough_name)
        )

        return {
            "hour": self._time_manager.get_hour(),
            "time_of_day": self._time_manager.get_time_of_the_day(),
            "local_information": self._local_information_factory.get_information(),
            "known_facts": facts_file,
            "relevant_characters_information": self._relevant_characters_information_factory.get_information(),
            "transcription": self._transcription.get_prettified_transcription(),
        }
