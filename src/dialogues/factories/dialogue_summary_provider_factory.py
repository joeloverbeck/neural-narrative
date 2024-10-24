from src.dialogues.providers.concrete_dialogue_summary_provider import (
    ConcreteDialogueSummaryProvider,
)
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)


class DialogueSummaryProviderFactory:

    def __init__(
        self, produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory
    ):
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_dialogue_summary_provider(
        self, transcription: Transcription
    ) -> ConcreteDialogueSummaryProvider:
        return ConcreteDialogueSummaryProvider(
            transcription, self._produce_tool_response_strategy_factory
        )
