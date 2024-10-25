from typing import Optional

from src.actions.products.action_resolution_product import ActionResolutionProduct
from src.base.playthrough_manager import PlaythroughManager
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.dialogues.participants import Participants


class StoreActionResolutionAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        store_character_memory_command_factory: StoreCharacterMemoryCommandFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._store_character_memory_command_factory = (
            store_character_memory_command_factory
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def do_algorithm(self, product: ActionResolutionProduct):
        for participant_identifier in self._participants.get_participant_keys():
            self._store_character_memory_command_factory.create_store_character_memory_command(
                participant_identifier, product.get_outcome()
            ).execute()
        self._playthrough_manager.add_to_adventure(product.get_outcome() + "\n")
