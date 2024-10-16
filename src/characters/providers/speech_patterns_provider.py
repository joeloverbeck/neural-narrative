from typing import Optional, Dict

from src.characters.products.speech_patterns_product import SpeechPatternsProduct
from src.constants import (
    SPEECH_PATTERNS_GENERATION_PROMPT_FILE,
    SPEECH_PATTERNS_GENERATION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
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

    def get_tool_file(self) -> str:
        return SPEECH_PATTERNS_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Generate 10 unique and compelling speech patterns that reflect the character's distinct narrative voice. Follow the provided instructions."

    def create_product(self, arguments: dict):
        return SpeechPatternsProduct(
            [
                arguments.get("speech_pattern_1"),
                arguments.get("speech_pattern_2"),
                arguments.get("speech_pattern_3"),
                arguments.get("speech_pattern_4"),
                arguments.get("speech_pattern_5"),
                arguments.get("speech_pattern_6"),
                arguments.get("speech_pattern_7"),
                arguments.get("speech_pattern_8"),
                arguments.get("speech_pattern_9"),
                arguments.get("speech_pattern_10"),
            ],
            is_valid=True,
        )

    def get_prompt_file(self) -> Optional[str]:
        return SPEECH_PATTERNS_GENERATION_PROMPT_FILE

    def get_prompt_kwargs(self) -> dict:
        return self._base_character_data
