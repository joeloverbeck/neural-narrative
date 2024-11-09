from typing import Optional, List

from src.base.abstracts.observer import Observer
from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.commands.produce_dialogue_command import ProduceDialogueCommand
from src.dialogues.composers.dialogue_turn_factory_composer import (
    DialogueTurnFactoryComposer,
)
from src.dialogues.composers.summarize_dialogue_command_factory_composer import (
    SummarizeDialogueCommandFactoryComposer,
)
from src.dialogues.factories.end_dialogue_command_factory import (
    EndDialogueCommandFactory,
)
from src.dialogues.factories.store_dialogues_command_factory import (
    StoreDialoguesCommandFactory,
)
from src.dialogues.factories.store_temporary_dialogue_command_factory import (
    StoreTemporaryDialogueCommandFactory,
)
from src.dialogues.participants import Participants


class ProduceDialogueCommandComposer:
    def __init__(
        self,
        playthrough_name: str,
        other_characters_identifiers: List[str],
        participants: Participants,
        purpose: Optional[str],
        dialogue_observer: Observer,
        player_input_factory: PlayerInputFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._other_characters_identifiers = other_characters_identifiers
        self._participants = participants
        self._purpose = purpose
        self._dialogue_observer = dialogue_observer
        self._player_input_factory = player_input_factory

    def compose_command(self) -> ProduceDialogueCommand:

        store_temporary_dialogue_command_factory = StoreTemporaryDialogueCommandFactory(
            self._playthrough_name, self._participants, self._purpose
        )

        dialogue_turn_factory = DialogueTurnFactoryComposer(
            self._playthrough_name,
            self._other_characters_identifiers,
            self._participants,
            self._purpose,
            self._dialogue_observer,
            self._player_input_factory,
        ).compose()

        summarize_dialogue_command_factory = SummarizeDialogueCommandFactoryComposer(
            self._playthrough_name,
            self._participants.get_participant_keys(),
        ).compose_factory()

        store_dialogues_command_factory = StoreDialoguesCommandFactory(
            self._playthrough_name, self._participants
        )

        end_dialogue_command_factory = EndDialogueCommandFactory(
            self._playthrough_name,
            summarize_dialogue_command_factory,
            store_dialogues_command_factory,
        )

        return ProduceDialogueCommand(
            self._playthrough_name,
            dialogue_turn_factory,
            store_temporary_dialogue_command_factory,
            end_dialogue_command_factory,
        )
