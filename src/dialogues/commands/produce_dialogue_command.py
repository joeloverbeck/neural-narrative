from src.abstracts.command import Command
from src.constants import TIME_ADVANCED_DUE_TO_DIALOGUE
from src.dialogues.abstracts.abstract_factories import DialogueFactory
from src.dialogues.commands.store_temporary_dialogue_command import (
    StoreTemporaryDialogueCommand,
)
from src.dialogues.factories.generate_interesting_situations_command_factory import (
    GenerateInterestingSituationsCommandFactory,
)
from src.dialogues.factories.store_dialogues_command_factory import (
    StoreDialoguesCommandFactory,
)
from src.dialogues.factories.summarize_dialogue_command_factory import (
    SummarizeDialogueCommandFactory,
)
from src.dialogues.participants import Participants
from src.filesystem.filesystem_manager import FilesystemManager
from src.time.time_manager import TimeManager


class ProduceDialogueCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
            purpose: str,
        dialogue_factory: DialogueFactory,
        summarize_dialogue_command_factory: SummarizeDialogueCommandFactory,
        store_dialogues_command_factory: StoreDialoguesCommandFactory,
            generate_interesting_situations_command_factory: GenerateInterestingSituationsCommandFactory,
        filesystem_manager: FilesystemManager = None,
        time_manager: TimeManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._dialogue_factory = dialogue_factory
        self._summarize_dialogue_command_factory = summarize_dialogue_command_factory
        self._store_dialogues_command_factory = store_dialogues_command_factory
        self._generate_interesting_situations_command_factory = (
            generate_interesting_situations_command_factory
        )

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._time_manager = time_manager or TimeManager(self._playthrough_name)

    def execute(self) -> None:
        dialogue_product = self._dialogue_factory.process_turn_of_dialogue()

        if dialogue_product.has_ended():
            self._summarize_dialogue_command_factory.create_summarize_dialogue_command(
                dialogue_product.get_transcription()
            ).execute()

            self._store_dialogues_command_factory.create_store_dialogues_command(
                dialogue_product.get_transcription()
            ).execute()

            # Must coax the LLM into creating interesting situations.
            self._generate_interesting_situations_command_factory.create_generate_interesting_situations_command(
                dialogue_product.get_transcription()
            ).execute()

            # Must remove the temporary dialogue.
            self._filesystem_manager.remove_ongoing_dialogue(self._playthrough_name)

            # Let's advance time, why not.
            self._time_manager.advance_time(TIME_ADVANCED_DUE_TO_DIALOGUE)

        else:
            # Must store the messages to the llm as well as the transcription as temporary.
            StoreTemporaryDialogueCommand(
                self._playthrough_name,
                self._participants,
                self._purpose,
                dialogue_product.get_messages_to_llm(),
                dialogue_product.get_transcription(),
            ).execute()
