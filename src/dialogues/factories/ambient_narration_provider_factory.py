from src.dialogues.providers.ambient_narration_provider import AmbientNarrationProvider
from src.dialogues.transcription import Transcription
from src.maps.place_description_manager import PlaceDescriptionManager
from src.maps.weathers_manager import WeathersManager
from src.prompting.factories.unparsed_string_produce_tool_response_strategy_factory import (
    UnparsedStringProduceToolResponseStrategyFactory,
)


class AmbientNarrationProviderFactory:

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: UnparsedStringProduceToolResponseStrategyFactory,
        weathers_manager: WeathersManager,
        place_description_manager: PlaceDescriptionManager,
    ):
        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )
        self._weathers_manager = weathers_manager
        self._place_description_manager = place_description_manager

    def create_provider(self, transcription: Transcription) -> AmbientNarrationProvider:
        return AmbientNarrationProvider(
            self._playthrough_name,
            transcription,
            self._produce_tool_response_strategy_factory,
            self._weathers_manager,
            self._place_description_manager,
        )
