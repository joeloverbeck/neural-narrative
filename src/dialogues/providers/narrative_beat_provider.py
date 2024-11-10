import logging
from pathlib import Path
from typing import Optional

from openai import BaseModel

from src.base.products.text_product import TextProduct
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


class NarrativeBeatProvider(BaseToolResponseProvider):
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
        return self._path_manager.get_narrative_beat_generation_prompt_path()

    def get_user_content(self) -> str:
        return "Write three or four sentences that naturally progress the actions of the characters, in the present tense, without including any dialogue. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        # Log chain of thought.
        logger.info(
            "Ambient narrative reasoning: %s",
            response_model.narrative_beat.chain_of_thought,
        )

        return TextProduct(response_model.narrative_beat.narrative_beat, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        return {
            "local_information": self._local_information_factory.get_information(),
            "player_and_followers_information": self._relevant_characters_information_factory.get_information(),
            "known_facts": self._format_known_facts_algorithm.do_algorithm(),
            "transcription": self._transcription.get_prettified_transcription(),
        }
