import logging

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.abstract_factories import DialogueTurnFactory
from src.dialogues.factories.end_dialogue_command_factory import (
    EndDialogueCommandFactory,
)
from src.dialogues.factories.store_temporary_dialogue_command_factory import (
    StoreTemporaryDialogueCommandFactory,
)

logger = logging.getLogger(__name__)


class ProduceDialogueCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        dialogue_turn_factory: DialogueTurnFactory,
        store_temporary_dialogue_command_factory: StoreTemporaryDialogueCommandFactory,
        end_dialogue_command_factory: EndDialogueCommandFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._dialogue_turn_factory = dialogue_turn_factory
        self._store_temporary_dialogue_command_factory = (
            store_temporary_dialogue_command_factory
        )
        self._end_dialogue_command_factory = end_dialogue_command_factory

    def execute(self) -> None:
        dialogue_product = self._dialogue_turn_factory.process_turn_of_dialogue()

        if dialogue_product.has_ended():
            self._end_dialogue_command_factory.create_command(
                dialogue_product
            ).execute()
        else:
            self._store_temporary_dialogue_command_factory.create_command(
                dialogue_product.get_transcription()
            ).execute()
