from typing import List

from src.base.validators import validate_non_empty_string, validate_list_of_str
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.databases.chroma_db_database import ChromaDbDatabase
from src.dialogues.factories.dialogue_summary_provider_factory import (
    DialogueSummaryProviderFactory,
)
from src.dialogues.factories.summarize_dialogue_command_factory import (
    SummarizeDialogueCommandFactory,
)
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms


class SummarizeDialogueCommandFactoryComposer:

    def __init__(self, playthrough_name: str, character_identifiers: List[str]):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_list_of_str(character_identifiers)

        self._playthrough_name = playthrough_name
        self._character_identifiers = character_identifiers

    def compose_factory(self) -> SummarizeDialogueCommandFactory:
        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_dialogue_summary(),
            ).compose_factory()
        )

        dialogue_summary_provider_factory = DialogueSummaryProviderFactory(
            produce_tool_response_strategy_factory
        )

        database = ChromaDbDatabase(self._playthrough_name)

        store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
            self._playthrough_name, database
        )

        return SummarizeDialogueCommandFactory(
            self._character_identifiers,
            dialogue_summary_provider_factory,
            store_character_memory_command_factory,
        )
