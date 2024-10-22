from typing import Optional
from src.base.constants import AMBIENT_NARRATION_GENERATION_PROMPT_FILE, AMBIENT_NARRATION_GENERATION_TOOL_FILE
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character import Character
from src.dialogues.products.ambient_narration_product import AmbientNarrationProduct
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.place_description_manager import PlaceDescriptionManager
from src.maps.weathers_manager import WeathersManager
from src.prompting.factories.produce_tool_response_strategy_factory import ProduceToolResponseStrategyFactory
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class AmbientNarrationProvider(BaseToolResponseProvider):

    def __init__(self, playthrough_name: str, transcription: Transcription,
                 produce_tool_response_strategy_factory:
                 ProduceToolResponseStrategyFactory, weathers_manager:
            WeathersManager, place_description_manager: PlaceDescriptionManager,
                 filesystem_manager: Optional[FilesystemManager] = None, time_manager:
            Optional[TimeManager] = None, playthrough_manager: Optional[
                PlaythroughManager] = None):
        super().__init__(produce_tool_response_strategy_factory,
                         filesystem_manager)
        self._playthrough_name = playthrough_name
        self._transcription = transcription
        self._weathers_manager = weathers_manager
        self._place_description_manager = place_description_manager
        self._time_manager = time_manager or TimeManager(self._playthrough_name
                                                         )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name)

    def get_prompt_file(self) -> str:
        return AMBIENT_NARRATION_GENERATION_PROMPT_FILE

    def get_tool_file(self) -> str:
        return AMBIENT_NARRATION_GENERATION_TOOL_FILE

    def get_user_content(self) -> str:
        return (
            'Write two or three sentences of ambient narration, as per the provided instructions.'
        )

    def create_product(self, arguments: dict):
        return AmbientNarrationProduct(arguments.get('ambient_narration'),
                                       is_valid=True)

    def get_prompt_kwargs(self) -> dict:
        setting_description = (self._place_description_manager.
                               get_place_description(self._playthrough_manager.
                                                     get_current_place_identifier()))
        personality = Character(self._playthrough_name, self.
                                _playthrough_manager.get_player_identifier()).personality
        return {'setting_description': setting_description, 'hour': self.
        _time_manager.get_hour(), 'time_of_day': self._time_manager.
        get_time_of_the_day(), 'weather': self._weathers_manager.
        get_weather_description(self._weathers_manager.
                                get_current_weather_identifier()), 'personality': personality,
                'transcription': self._transcription.get_prettified_transcription()
                }
