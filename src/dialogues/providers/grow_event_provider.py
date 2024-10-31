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
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class GrowEventProvider(BaseToolResponseProvider):
    def __init__(
        self,
        suggested_event: str,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        relevant_characters_information_factory: RelevantCharactersInformationFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(
            produce_tool_response_strategy_factory, filesystem_manager, path_manager
        )

        validate_non_empty_string(suggested_event, "suggested_event")

        self._suggested_event = suggested_event
        self._transcription = transcription
        self._local_information_factory = local_information_factory
        self._relevant_characters_information_factory = (
            relevant_characters_information_factory
        )

    def get_prompt_file(self) -> Path:
        return self._path_manager.get_grow_event_prompt_path()

    def get_user_content(self) -> str:
        return f"User's suggested event: {self._suggested_event}.\nYour task: Expand the user's suggested event into a third-person narrative text of four or five sentences, written in the present tense, that seamlessly integrates into the ongoing story."

    def create_product_from_base_model(self, response_model: BaseModel):
        # Log chain of thought.
        logger.info(
            "Grow event reasoning: %s",
            response_model.grow_event.chain_of_thought,
        )

        return TextProduct(response_model.grow_event.event, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        return {
            "local_information": self._local_information_factory.get_information(),
            "relevant_characters_information": self._relevant_characters_information_factory.get_information(),
            "transcription": self._transcription.get_prettified_transcription(),
        }