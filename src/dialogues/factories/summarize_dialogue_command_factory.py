from typing import List

from src.characters.commands.summarize_dialogue_command import SummarizeDialogueCommand
from src.characters.factories.store_character_memory_command_factory import StoreCharacterMemoryCommandFactory
from src.dialogues.factories.dialogue_summary_provider_factory import DialogueSummaryProviderFactory
from src.dialogues.transcription import Transcription


class SummarizeDialogueCommandFactory:
    def __init__(self, participants: List[str], dialogue_summary_provider_factory: DialogueSummaryProviderFactory,
                 store_character_memory_command_factory: StoreCharacterMemoryCommandFactory):
        if len(participants) < 2:
            raise ValueError("There should be at least two participants in the dialogue.")

        self._participants = participants
        self._dialogue_summary_provider_factory = dialogue_summary_provider_factory
        self._store_character_memory_command_factory = store_character_memory_command_factory

    def create_summarize_dialogue_command(self, transcription: Transcription) -> SummarizeDialogueCommand:
        return SummarizeDialogueCommand(self._participants,
                                        transcription,
                                        self._dialogue_summary_provider_factory,
                                        self._store_character_memory_command_factory)
