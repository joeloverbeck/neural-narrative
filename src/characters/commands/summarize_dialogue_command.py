import logging
from typing import List

from src.base.abstracts.command import Command
from src.base.validators import validate_list_of_str
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.dialogues.factories.dialogue_summary_provider_factory import (
    DialogueSummaryProviderFactory,
)
from src.dialogues.models.dialogue_summary import DialogueSummary
from src.dialogues.transcription import Transcription

logger = logging.getLogger(__name__)


class SummarizeDialogueCommand(Command):

    def __init__(
        self,
        character_identifiers: List[str],
        transcription: Transcription,
        dialogue_summary_provider_factory: DialogueSummaryProviderFactory,
        store_character_memory_command_factory: StoreCharacterMemoryCommandFactory,
    ):
        validate_list_of_str(character_identifiers)

        self._character_identifiers = character_identifiers
        self._transcription = transcription
        self._dialogue_summary_provider_factory = dialogue_summary_provider_factory
        self._store_character_memory_command_factory = (
            store_character_memory_command_factory
        )

    def execute(self) -> None:
        if not self._transcription.is_transcription_sufficient():
            logger.warning(
                "Won't create memories out of an empty dialogue or insufficient dialogue."
            )
            return

        summary_product = (
            self._dialogue_summary_provider_factory.create_dialogue_summary_provider(
                self._transcription
            ).generate_product(DialogueSummary)
        )

        if not summary_product.is_valid():
            raise ValueError(
                f"Failed to create a summary for the dialogue: {summary_product.get_error()}"
            )

        for participant_identifier in self._character_identifiers:
            self._store_character_memory_command_factory.create_store_character_memory_command(
                participant_identifier, summary_product.get()
            ).execute()
