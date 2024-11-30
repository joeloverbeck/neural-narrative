from typing import Dict, Any, Optional

from src.base.abstracts.command import Command
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.characters.characters_manager import CharactersManager
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


class ProcessGeneratedCharacterDataCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_data: Dict[str, Any],
        place_character_at_current_place: bool,
        store_generated_character_command_factory: StoreGeneratedCharacterCommandFactory,
        generate_character_image_command_factory: GenerateCharacterImageCommandFactory,
        place_character_at_place_command_factory: PlaceCharacterAtPlaceCommandFactory,
        characters_manager: Optional[CharactersManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._character_data = character_data
        self._place_character_at_current_place = place_character_at_current_place
        self._store_generated_character_command_factory = (
            store_generated_character_command_factory
        )
        self._generate_character_image_command_factory = (
            generate_character_image_command_factory
        )
        self._place_character_at_place_command_factory = (
            place_character_at_place_command_factory
        )

        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )

    def execute(self) -> None:
        self._store_generated_character_command_factory.create_store_generated_character_command(
            self._character_data
        ).execute()

        # Generate the character's image.
        self._generate_character_image_command_factory.create_command(
            self._characters_manager.get_latest_character_identifier()
        ).execute()

        if self._place_character_at_current_place:
            current_place = self._playthrough_manager.get_current_place_identifier()

            self._place_character_at_place_command_factory.create_command(
                self._characters_manager.get_latest_character_identifier(),
                current_place,
            ).execute()
