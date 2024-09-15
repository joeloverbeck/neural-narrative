from src.abstracts.command import Command
from src.dialogues.abstracts.abstract_factories import DialogueFactory
from src.dialogues.commands.store_temporary_dialogue_command import StoreTemporaryDialogueCommand
from src.dialogues.factories.store_dialogues_command_factory import StoreDialoguesCommandFactory
from src.dialogues.factories.summarize_dialogue_command_factory import SummarizeDialogueCommandFactory
from src.dialogues.participants import Participants
from src.filesystem.filesystem_manager import FilesystemManager


class ProduceDialogueCommand(Command):
    def __init__(self, playthrough_name: str, participants: Participants, dialogue_factory: DialogueFactory,
                 summarize_dialogue_command_factory: SummarizeDialogueCommandFactory,
                 store_dialogues_command_factory: StoreDialoguesCommandFactory,
                 filesystem_manager: FilesystemManager = None):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._dialogue_factory = dialogue_factory
        self._summarize_dialogue_command_factory = summarize_dialogue_command_factory
        self._store_dialogues_command_factory = store_dialogues_command_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        dialogue_product = self._dialogue_factory.process_turn_of_dialogue()

        if dialogue_product.has_ended():
            # Must create summary, as well as store the transcription permanently.
            self._summarize_dialogue_command_factory.create_summarize_dialogue_command(
                dialogue_product.get_transcription()).execute()

            self._store_dialogues_command_factory.create_store_dialogues_command(
                dialogue_product.get_transcription()).execute()

            # Must remove the temporary dialogue.
            self._filesystem_manager.remove_ongoing_dialogue(self._playthrough_name)
        else:
            # Must store the messages to the llm as well as the transcription as temporary.
            StoreTemporaryDialogueCommand(self._playthrough_name, self._participants,
                                          dialogue_product.get_messages_to_llm(),
                                          dialogue_product.get_transcription()).execute()
