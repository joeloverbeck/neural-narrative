from src.dialogues.providers.summary_note_provider import SummaryNoteProvider
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class SummaryNoteProviderFactory:
    def __init__(
        self, produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_provider(
        self, transcription: Transcription, speaker_name: str
    ) -> SummaryNoteProvider:
        return SummaryNoteProvider(
            transcription, speaker_name, self._produce_tool_response_strategy_factory
        )
