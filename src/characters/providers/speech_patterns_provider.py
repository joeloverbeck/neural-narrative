from pathlib import Path
from typing import Optional, Dict

from pydantic import BaseModel

from src.characters.products.speech_patterns_product import SpeechPatternsProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.filesystem.path_manager import PathManager
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
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(
            produce_tool_response_strategy_factory, filesystem_manager, path_manager
        )

        self._base_character_data = base_character_data

    def get_user_content(self) -> str:
        return "Generate 10 unique and compelling speech patterns that reflect the character's distinct narrative voice. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return SpeechPatternsProduct(
            response_model.speech_patterns,
            is_valid=True,
        )

    def get_prompt_file(self) -> Optional[Path]:
        return self._path_manager.get_speech_patterns_generation_prompt_path()

    def get_prompt_kwargs(self) -> dict:
        return self._base_character_data
