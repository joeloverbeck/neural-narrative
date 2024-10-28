from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.commands.store_temporary_dialogue_command import (
    StoreTemporaryDialogueCommand,
)
from src.dialogues.factories.load_ongoing_conversation_data_command_factory import (
    LoadOngoingConversationDataCommandFactory,
)
from src.dialogues.observers.web_narration_observer import (
    WebNarrationObserver,
)
from src.dialogues.transcription import Transcription


class ProduceNarrationForDialogueCommand(Command):

    def __init__(
        self,
        message_type: str,
        transcription: Transcription,
        web_ambient_narration_observer: WebNarrationObserver,
        narration_for_dialogue_strategy: NarrationForDialogueStrategy,
        handle_possible_existence_of_ongoing_conversation_command_factory: LoadOngoingConversationDataCommandFactory,
        store_temporary_dialogue_command: StoreTemporaryDialogueCommand,
    ):
        validate_non_empty_string(message_type, "message_type")

        self._message_type = message_type
        self._transcription = transcription
        self._web_ambient_narration_observer = web_ambient_narration_observer
        self._narration_for_dialogue_strategy = narration_for_dialogue_strategy
        (self._handle_possible_existence_of_ongoing_conversation_command_factory) = (
            handle_possible_existence_of_ongoing_conversation_command_factory
        )
        self._store_temporary_dialogue_command = store_temporary_dialogue_command

    def execute(self) -> None:
        self._handle_possible_existence_of_ongoing_conversation_command_factory.create_handle_possible_existence_of_ongoing_conversation_command(
            self._transcription
        ).execute()

        narration = self._narration_for_dialogue_strategy.produce_narration()

        self._web_ambient_narration_observer.update(
            {
                "alignment": "center",
                "message_text": narration,
                "message_type": self._message_type,
            }
        )

        self._transcription.add_line(narration)

        self._store_temporary_dialogue_command.execute()
