from typing import Optional

from src.constants import (
    INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE,
    INTERESTING_SITUATIONS_GENERATION_TOOL_FILE,
)
from src.dialogues.transcription import Transcription
from src.events.products.interesting_situations_product import (
    InterestingSituationsProduct,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class InterestingSituationsFactory(BaseToolResponseProvider):
    def __init__(
        self,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)
        self._transcription = transcription

    def get_prompt_file(self) -> str:
        return INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        return {"transcription": self._transcription.get()}

    def get_tool_file(self) -> str:
        return INTERESTING_SITUATIONS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            "Write a list of at least five very interesting and intriguing situations "
            "that could stem from this conversation, as per the above instructions."
        )

    def create_product(self, arguments: dict):
        return InterestingSituationsProduct(
            arguments.get("interesting_situations"), is_valid=True
        )
