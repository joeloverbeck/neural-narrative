from typing import Optional

from pydantic import BaseModel

from src.base.constants import (
    SUMMARIZE_DIALOGUE_PROMPT_FILE,
)
from src.dialogues.models.dialogue_summary import DialogueSummary
from src.dialogues.products.concrete_summary_product import ConcreteSummaryProduct
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ConcreteDialogueSummaryProvider(BaseToolResponseProvider):
    def __init__(
        self,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._transcription = transcription

    def get_prompt_file(self) -> str:
        return SUMMARIZE_DIALOGUE_PROMPT_FILE

    def _get_tool_data(self) -> dict:
        return DialogueSummary.model_json_schema()

    def get_user_content(self) -> str:
        return "Summarize the provided dialogue. Do not write any preamble, just do it as instructed."

    def get_prompt_kwargs(self) -> dict:
        return {"transcription": self._transcription.get_prettified_transcription()}

    def create_product_from_base_model(self, base_model: BaseModel):
        return ConcreteSummaryProduct(base_model.summary, is_valid=True)
