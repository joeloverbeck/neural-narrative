import logging
from typing import Optional
from src.base.abstracts.command import Command
from src.base.constants import TIME_ADVANCED_DUE_TO_DIALOGUE
from src.dialogues.abstracts.abstract_factories import DialogueTurnFactory
from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.commands.store_temporary_dialogue_command import StoreTemporaryDialogueCommand
from src.dialogues.factories.store_dialogues_command_factory import StoreDialoguesCommandFactory
from src.dialogues.factories.summarize_dialogue_command_factory import SummarizeDialogueCommandFactory
from src.dialogues.participants import Participants
from src.filesystem.filesystem_manager import FilesystemManager
from src.time.time_manager import TimeManager
logger = logging.getLogger(__name__)


class ProduceDialogueCommand(Command):

    def __init__(self, playthrough_name: str, participants: Participants,
                 purpose: Optional[str], dialogue_turn_factory: DialogueTurnFactory,
        summarize_dialogue_command_factory: SummarizeDialogueCommandFactory,
        store_dialogues_command_factory: StoreDialoguesCommandFactory,
                 filesystem_manager: Optional[FilesystemManager] = None, time_manager:
            Optional[TimeManager] = None):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not participants.enough_participants():
            raise ValueError('Not enough participants.')
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._dialogue_turn_factory = dialogue_turn_factory
        self._summarize_dialogue_command_factory = (
            summarize_dialogue_command_factory)
        self._store_dialogues_command_factory = store_dialogues_command_factory
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._time_manager = time_manager or TimeManager(self._playthrough_name
                                                         )

    def _process_end_of_dialogue(self, dialogue_product: DialogueProduct):
        if dialogue_product.get_transcription().is_transcription_sufficient():
            self._summarize_dialogue_command_factory.create_summarize_dialogue_command(
                dialogue_product.get_transcription()).execute()
            self._store_dialogues_command_factory.create_store_dialogues_command(
                dialogue_product.get_transcription()).execute()
        self._filesystem_manager.remove_ongoing_dialogue(self._playthrough_name
                                                         )
        self._time_manager.advance_time(TIME_ADVANCED_DUE_TO_DIALOGUE)

    def execute(self) -> None:
        dialogue_product = (self._dialogue_turn_factory.
                            process_turn_of_dialogue())
        if dialogue_product.has_ended():
            self._process_end_of_dialogue(dialogue_product)
        else:
            StoreTemporaryDialogueCommand(self._playthrough_name, self.
                                          _participants, self._purpose, dialogue_product.
                                          get_messages_to_llm(), dialogue_product.get_transcription()
                                          ).execute()
