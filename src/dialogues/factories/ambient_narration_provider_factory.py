from src.dialogues.providers.ambient_narration_provider import AmbientNarrationProvider
from src.dialogues.transcription import Transcription
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class AmbientNarrationProviderFactory:
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_provider(self, transcription: Transcription) -> AmbientNarrationProvider:
        return AmbientNarrationProvider(
            self._playthrough_name,
            transcription,
            self._produce_tool_response_strategy_factory,
        )
