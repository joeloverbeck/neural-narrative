from typing import Dict, cast, Optional

from src.actions.factories.goal_resolution_factory import GoalResolutionFactory
from src.actions.products.goal_resolution_product import GoalResolutionProduct
from src.characters.characters_manager import CharactersManager
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.dialogues.participants import Participants
from src.playthrough_manager import PlaythroughManager


class ProduceGoalResolutionAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        goal_resolution_factory: GoalResolutionFactory,
        store_character_memory_command_factory: StoreCharacterMemoryCommandFactory,
        characters_manager: Optional[CharactersManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        if not len(participants.get_participant_keys()) >= 1:
            raise ValueError(
                f"There should be at least one person attempting to resolve this goal. Participants: {participants.get()}"
            )

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._goal_resolution_factory = goal_resolution_factory
        self._store_character_memory_command_factory = (
            store_character_memory_command_factory
        )

        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def produce_goal_resolution(self) -> Dict[str, str]:
        product = cast(
            GoalResolutionProduct, self._goal_resolution_factory.generate_product()
        )

        if not product.is_valid():
            raise ValueError(
                f"Was unable to generate goal resolution. Error: {product.get_error()}"
            )

        # The product should contain "narration", "success_determination", and "resolution".
        for participant_identifier in self._participants.get_participant_keys():
            self._store_character_memory_command_factory.create_store_character_memory_command(
                participant_identifier, product.get()["resolution"]
            ).execute()

        # Should add the narration and the resolution to the ongoing adventure.
        self._playthrough_manager.add_to_adventure(product.get()["narration"] + "\n")
        self._playthrough_manager.add_to_adventure(product.get()["resolution"] + "\n")

        # Return the data in case the user wants it for something.
        return product.get()
