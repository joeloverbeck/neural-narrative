from typing import Optional

from pydantic import BaseModel

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.dialogues.products.ambient_narration_product import AmbientNarrationProduct
from src.dialogues.transcription import Transcription
from src.filesystem.path_manager import PathManager
from src.maps.factories.local_information_factory import LocalInformationFactory
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class AmbientNarrationProvider(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        local_information_factory: LocalInformationFactory,
        path_manager: Optional[PathManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        self._playthrough_name = playthrough_name
        self._transcription = transcription
        self._local_information_factory = local_information_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def get_prompt_file(self) -> str:
        return self._path_manager.get_ambient_narration_generation_prompt_path()

    def get_user_content(self) -> str:
        return "Write two or three sentences of ambient narration, as per the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return AmbientNarrationProduct(response_model.ambient_narration, is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        personality = Character(
            self._playthrough_name, self._playthrough_manager.get_player_identifier()
        ).personality

        return {
            "local_information": self._local_information_factory.get_information(),
            "personality": personality,
            "transcription": self._transcription.get_prettified_transcription(),
        }
