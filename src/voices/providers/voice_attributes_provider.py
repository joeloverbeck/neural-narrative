from typing import Optional, Dict

from pydantic import BaseModel

from src.base.products.dict_product import DictProduct
from src.filesystem.path_manager import PathManager
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class VoiceAttributesProvider(BaseToolResponseProvider):

    def __init__(
        self,
        base_character_data: Dict[str, str],
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._base_character_data = base_character_data

    def get_prompt_file(self) -> str:
        return self._path_manager.get_voice_attributes_generation_prompt_path()

    def get_user_content(self) -> str:
        return f"Pick the most fitting voice attributes for {self._base_character_data["name"]} from the provided options."

    def create_product_from_base_model(self, response_model: BaseModel):
        arguments = {
            "voice_gender": response_model.voice_gender,
            "voice_age": response_model.voice_age,
            "voice_emotion": response_model.voice_emotion,
            "voice_tempo": response_model.voice_tempo,
            "voice_volume": response_model.voice_volume,
            "voice_texture": response_model.voice_texture,
            "voice_tone": response_model.voice_tone,
            "voice_style": response_model.voice_style,
            "voice_personality": response_model.voice_personality,
            "voice_special_effects": response_model.voice_special_effects,
        }

        return DictProduct(arguments, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        return self._base_character_data
