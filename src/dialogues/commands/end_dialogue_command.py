from typing import Optional

from src.base.abstracts.command import Command
from src.base.validators import validate_non_empty_string
from src.dialogues.abstracts.factory_products import DialogueProduct
from src.dialogues.factories.store_dialogues_command_factory import (
    StoreDialoguesCommandFactory,
)
from src.dialogues.factories.summarize_dialogue_command_factory import (
    SummarizeDialogueCommandFactory,
)
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)
from src.filesystem.config_loader import ConfigLoader
from src.time.time_manager import TimeManager


class EndDialogueCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        dialogue_product: DialogueProduct,
        summarize_dialogue_command_factory: SummarizeDialogueCommandFactory,
        store_dialogues_command_factory: StoreDialoguesCommandFactory,
        ongoing_dialogue_repository: Optional[OngoingDialogueRepository] = None,
        time_manager: Optional[TimeManager] = None,
        config_loader: Optional[ConfigLoader] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._dialogue_product = dialogue_product
        self._summarize_dialogue_command_factory = summarize_dialogue_command_factory
        self._store_dialogues_command_factory = store_dialogues_command_factory

        self._ongoing_dialogue_repository = (
            ongoing_dialogue_repository or OngoingDialogueRepository(playthrough_name)
        )
        self._time_manager = time_manager or TimeManager(playthrough_name)
        self._config_loader = config_loader or ConfigLoader()

    def execute(self) -> None:
        if self._dialogue_product.get_transcription().is_transcription_sufficient():
            self._summarize_dialogue_command_factory.create_summarize_dialogue_command(
                self._dialogue_product.get_transcription()
            ).execute()

            self._store_dialogues_command_factory.create_command(
                self._dialogue_product.get_transcription()
            ).execute()

        self._ongoing_dialogue_repository.remove_dialogue()

        self._time_manager.advance_time(
            self._config_loader.get_time_advanced_due_to_dialogue()
        )
