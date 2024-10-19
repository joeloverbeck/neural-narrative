import logging

from src.base.abstracts.command import Command
from src.characters.factories.store_character_memory_command_factory import StoreCharacterMemoryCommandFactory
from src.dialogues.factories.dialogue_summary_provider_factory import DialogueSummaryProviderFactory
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription

logger = logging.getLogger(__name__)


class SummarizeDialogueCommand(Command):

    def __init__(self, participants: Participants,
                 transcription: Transcription, dialogue_summary_provider_factory: DialogueSummaryProviderFactory,
                 store_character_memory_command_factory: StoreCharacterMemoryCommandFactory):
        if not participants.enough_participants():
            raise ValueError("There weren't enough participants.")

        self._participants = participants
        self._transcription = transcription
        self._dialogue_summary_provider_factory = dialogue_summary_provider_factory
        self._store_character_memory_command_factory = store_character_memory_command_factory

    def execute(self) -> None:
        # Once the chat is over, the LLM should be prompted to create a memory out of it for all participants.
        if not self._transcription.is_transcription_sufficient():
            # Perhaps the dialogue is empty. In that case, no summary needs to be done.
            logger.warning("Won't create memories out of an empty dialogue or insufficient dialogue.")
            return

        summary_product = self._dialogue_summary_provider_factory.create_dialogue_summary_provider(
            self._transcription).create_summary()

        if not summary_product.is_valid():
            raise ValueError(f"Failed to create a summary for the dialogue: {summary_product.get_error()}")

        # Now that we have the summary, gotta add it to the memories of all participants.
        for participant_identifier in self._participants.get_participant_keys():
            self._store_character_memory_command_factory.create_store_character_memory_command(participant_identifier,
                                                                                               summary_product.get()).execute()
