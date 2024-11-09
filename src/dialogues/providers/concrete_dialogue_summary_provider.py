from typing import Optional

from pydantic import BaseModel

from src.base.products.text_product import TextProduct
from src.dialogues.transcription import Transcription
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ConcreteDialogueSummaryProvider(BaseToolResponseProvider):
    def __init__(
        self,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._transcription = transcription

    def get_prompt_file(self) -> str:
        return self._path_manager.get_summarize_dialogue_prompt_path()

    def get_user_content(self) -> str:
        return "Summarize the provided dialogue. Do not write any preamble, just do it as instructed."

    def get_prompt_kwargs(self) -> dict:
        return {"transcription": self._transcription.get_prettified_transcription()}

    def create_product_from_base_model(self, response_model: BaseModel):
        return TextProduct(response_model.summary, is_valid=True)
