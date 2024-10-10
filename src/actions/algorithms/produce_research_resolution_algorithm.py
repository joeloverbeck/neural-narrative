from typing import cast, Optional

from src.actions.factories.research_resolution_factory import ResearchResolutionFactory
from src.actions.products.research_resolution_product import ResearchResolutionProduct
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.constants import NARRATOR_VOICE_MODEL
from src.dialogues.participants import Participants
from src.playthrough_manager import PlaythroughManager
from src.services.voices_services import VoicesServices


class ProduceResearchResolutionAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        research_resolution_factory: ResearchResolutionFactory,
        store_character_memory_command_factory: StoreCharacterMemoryCommandFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._research_resolution_factory = research_resolution_factory
        self._store_character_memory_command_factory = (
            store_character_memory_command_factory
        )

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def do_algorithm(self) -> ResearchResolutionProduct:
        product = cast(
            ResearchResolutionProduct,
            self._research_resolution_factory.generate_product(),
        )

        if not product.is_valid():
            raise ValueError(
                f"The generation of a research resolution failed. Error: {product.get_error()}"
            )

        # At this point we have a valid research resolution.

        # Store both outcome and consequences as memories for all involved.
        for participant_identifier in self._participants.get_participant_keys():
            self._store_character_memory_command_factory.create_store_character_memory_command(
                participant_identifier, product.get_outcome()
            ).execute()
            self._store_character_memory_command_factory.create_store_character_memory_command(
                participant_identifier, product.get_consequences()
            ).execute()

        self._playthrough_manager.add_to_adventure(product.get_outcome() + "\n")
        self._playthrough_manager.add_to_adventure(product.get_consequences() + "\n")

        # At this point we can also produce the voice lines
        VoicesServices().generate_voice_line(
            "narrator", product.get_narrative(), NARRATOR_VOICE_MODEL
        )
        VoicesServices().generate_voice_line(
            "narrator", product.get_outcome(), NARRATOR_VOICE_MODEL
        )
        VoicesServices().generate_voice_line(
            "narrator", product.get_consequences(), NARRATOR_VOICE_MODEL
        )

        return product
