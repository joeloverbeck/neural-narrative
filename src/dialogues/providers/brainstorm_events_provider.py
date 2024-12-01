import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.base.products.texts_product import TextsProduct
from src.base.tools import join_with_newline
from src.characters.factories.relevant_characters_information_factory import (
    RelevantCharactersInformationFactory,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.dialogues.transcription import Transcription
from src.filesystem.path_manager import PathManager
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class BrainstormEventsProvider(BaseToolResponseProvider):
    def __init__(
        self,
        transcription: Transcription,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        relevant_characters_information_factory: RelevantCharactersInformationFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._transcription = transcription
        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._local_information_factory = local_information_factory
        self._relevant_characters_information_factory = (
            relevant_characters_information_factory
        )

    def get_prompt_file(self) -> Path:
        return self._path_manager.get_brainstorm_events_prompt_path()

    def get_user_content(self) -> str:
        return "Based on the information provided, brainstorm possible, distinct events that would naturally follow from the ongoing dialogue and context."

    def create_product_from_base_model(self, response_model: BaseModel):
        return TextsProduct(response_model.events, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        local_information = self._local_information_factory.get_information()

        transcription = self._transcription.get_transcription_excerpt()

        known_facts = self._format_known_facts_algorithm.do_algorithm(
            join_with_newline(local_information, transcription)
        )

        relevant_characters_information = (
            self._relevant_characters_information_factory.get_information(
                join_with_newline(local_information, transcription, known_facts)
            )
        )

        return {
            "local_information": local_information,
            "relevant_characters_information": relevant_characters_information,
            "known_facts": known_facts,
            "transcription": transcription,
        }
