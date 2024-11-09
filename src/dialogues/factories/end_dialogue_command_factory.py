from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.commands.end_dialogue_command import EndDialogueCommand
from src.dialogues.factories.store_dialogues_command_factory import (
    StoreDialoguesCommandFactory,
)
from src.dialogues.factories.summarize_dialogue_command_factory import (
    SummarizeDialogueCommandFactory,
)


class EndDialogueCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        summarize_dialogue_command_factory: SummarizeDialogueCommandFactory,
        store_dialogues_command_factory: StoreDialoguesCommandFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._summarize_dialogue_command_factory = summarize_dialogue_command_factory
        self._store_dialogues_command_factory = store_dialogues_command_factory

    def create_command(self, dialogue_product: DialogueProduct) -> EndDialogueCommand:
        return EndDialogueCommand(
            self._playthrough_name,
            dialogue_product,
            self._summarize_dialogue_command_factory,
            self._store_dialogues_command_factory,
        )
