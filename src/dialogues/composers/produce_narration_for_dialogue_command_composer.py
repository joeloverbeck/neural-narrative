from typing import Optional, List

from src.base.validators import validate_non_empty_string, validate_list_of_str
from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.commands.produce_narration_for_dialogue_command import (
    ProduceNarrationForDialogueCommand,
)
from src.dialogues.commands.store_temporary_dialogue_command import (
    StoreTemporaryDialogueCommand,
)
from src.dialogues.composers.load_or_initialize_dialogue_data_command_factory_composer import (
    LoadOrInitializeDialogueDataCommandFactoryComposer,
)
from src.dialogues.observers.web_narration_observer import WebNarrationObserver
from src.dialogues.participants import Participants
from src.dialogues.transcription import Transcription


class ProduceNarrationForDialogueCommandComposer:
    def __init__(
        self,
        playthrough_name: str,
        other_characters_identifiers: List[str],
        purpose: Optional[str],
        message_type: str,
        web_narration_observer: WebNarrationObserver,
        narration_for_dialogue_strategy: NarrationForDialogueStrategy,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_list_of_str(other_characters_identifiers)
        validate_non_empty_string(message_type, "message_type")

        self._playthrough_name = playthrough_name
        self._other_characters_identifiers = other_characters_identifiers
        self._purpose = purpose
        self._message_type = message_type
        self._web_narration_observer = web_narration_observer
        self._narration_for_dialogue_strategy = narration_for_dialogue_strategy

    def compose_command(self) -> ProduceNarrationForDialogueCommand:
        transcription = Transcription()
        participants = Participants()

        load_or_initialize_dialogue_data_command_factory = (
            LoadOrInitializeDialogueDataCommandFactoryComposer(
                self._playthrough_name, self._other_characters_identifiers, participants
            ).compose_factory()
        )

        store_temporary_dialogue_command = StoreTemporaryDialogueCommand(
            self._playthrough_name,
            participants,
            self._purpose,
            transcription,
        )

        return ProduceNarrationForDialogueCommand(
            self._message_type,
            transcription,
            self._web_narration_observer,
            self._narration_for_dialogue_strategy,
            load_or_initialize_dialogue_data_command_factory,
            store_temporary_dialogue_command,
        )
