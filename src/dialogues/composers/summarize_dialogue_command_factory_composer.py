from src.base.validators import validate_non_empty_string
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.dialogues.factories.dialogue_summary_provider_factory import (
    DialogueSummaryProviderFactory,
)
from src.dialogues.factories.summarize_dialogue_command_factory import (
    SummarizeDialogueCommandFactory,
)
from src.dialogues.participants import Participants
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms


class SummarizeDialogueCommandFactoryComposer:

    def __init__(self, playthrough_name: str, participants: Participants):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._participants = participants

    def compose_factory(self) -> SummarizeDialogueCommandFactory:
        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_dialogue_summary(),
            ).compose_factory()
        )

        dialogue_summary_provider_factory = DialogueSummaryProviderFactory(
            produce_tool_response_strategy_factory
        )

        store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
            self._playthrough_name
        )

        return SummarizeDialogueCommandFactory(
            self._participants,
            dialogue_summary_provider_factory,
            store_character_memory_command_factory,
        )
