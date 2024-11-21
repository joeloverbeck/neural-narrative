import logging
from pathlib import Path
from typing import Optional

from openai import BaseModel

from src.base.products.dict_product import DictProduct
from src.base.validators import validate_non_empty_string
from src.dialogues.transcription import Transcription
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class SummaryNoteProvider(BaseToolResponseProvider):
    def __init__(
        self,
        transcription: Transcription,
        speaker_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        validate_non_empty_string(speaker_name, "speaker_name")

        self._transcription = transcription
        self._speaker_name = speaker_name

    def get_prompt_file(self) -> Path:
        return self._path_manager.get_summary_note_generation_prompt_path()

    def get_user_content(self) -> str:
        return f"Produce a summary note describing the inferences {self._speaker_name} can make about all the other participants. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return DictProduct(response_model.inferences, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        return {
            "transcription_excerpt": self._transcription.get_transcription_excerpt(),
            "name": self._speaker_name,
        }
