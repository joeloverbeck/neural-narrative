from typing import Optional

from src.characters.characters_manager import CharactersManager
from src.constants import (
    AMBIENT_NARRATION_GENERATION_PROMPT_FILE,
    AMBIENT_NARRATION_GENERATION_TOOL_FILE,
)
from src.dialogues.products.ambient_narration_product import AmbientNarrationProduct
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class AmbientNarrationProvider(BaseToolResponseProvider):
    def __init__(
        self,
        playthrough_name: str,
        transcription: Transcription,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        time_manager: Optional[TimeManager] = None,
        map_manager: Optional[MapManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._transcription = transcription

        self._time_manager = time_manager or TimeManager(self._playthrough_name)
        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def get_prompt_file(self) -> str:
        return AMBIENT_NARRATION_GENERATION_PROMPT_FILE

    def get_tool_file(self) -> str:
        return AMBIENT_NARRATION_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Write a couple of sentences of ambient narration, as per the provided instructions."

    def create_product(self, arguments: dict):
        return AmbientNarrationProduct(
            arguments.get("ambient_narration"), is_valid=True
        )

    def get_prompt_kwargs(self) -> dict:
        setting_description = self._map_manager.get_place_description(
            self._playthrough_manager.get_current_place_identifier()
        )

        personality = self._characters_manager.load_character_data(
            self._playthrough_manager.get_player_identifier()
        ).get("personality")

        return {
            "setting_description": setting_description,
            "hour": self._time_manager.get_hour(),
            "time_of_day": self._time_manager.get_time_of_the_day(),
            "personality": personality,
            "transcription": self._transcription.get_prettified_transcription(),
        }
