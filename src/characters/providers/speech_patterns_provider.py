from typing import Optional, Dict

from pydantic import BaseModel

from src.base.constants import (
    SPEECH_PATTERNS_GENERATION_PROMPT_FILE,
)
from src.characters.models.speech_patterns import SpeechPatterns
from src.characters.products.speech_patterns_product import SpeechPatternsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class SpeechPatternsProvider(BaseToolResponseProvider):

    def __init__(
        self,
        base_character_data: Dict[str, str],
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        self._base_character_data = base_character_data

    def _get_tool_data(self) -> dict:
        return SpeechPatterns.model_json_schema()

    def get_user_content(self) -> str:
        return "Generate 10 unique and compelling speech patterns that reflect the character's distinct narrative voice. Follow the provided instructions."

    def create_product_from_base_model(self, base_model: BaseModel):
        return SpeechPatternsProduct(
            base_model.speech_patterns,
            is_valid=True,
        )

    def get_prompt_file(self) -> Optional[str]:
        return SPEECH_PATTERNS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        return self._base_character_data
