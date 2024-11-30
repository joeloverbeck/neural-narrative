from typing import Dict, Any

from src.base.validators import validate_non_empty_string
from src.characters.commands.process_generated_character_data_command import (
    ProcessGeneratedCharacterDataCommand,
)
from src.characters.factories.store_generated_character_command_factory import (
    StoreGeneratedCharacterCommandFactory,
)
from src.images.factories.generate_character_image_command_factory import (
    GenerateCharacterImageCommandFactory,
)
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


class ProcessGeneratedCharacterDataCommandFactory:
    def __init__(
        self,
        playthrough_name: str,
        store_generated_character_command_factory: StoreGeneratedCharacterCommandFactory,
        generate_character_image_command_factory: GenerateCharacterImageCommandFactory,
        place_character_at_place_command_factory: PlaceCharacterAtPlaceCommandFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._store_generated_character_command_factory = (
            store_generated_character_command_factory
        )
        self._generate_character_image_command_factory = (
            generate_character_image_command_factory
        )
        self._place_character_at_place_command_factory = (
            place_character_at_place_command_factory
        )

    def create_command(
        self, character_data: Dict[str, Any], place_character_at_current_place: bool
    ) -> ProcessGeneratedCharacterDataCommand:
        return ProcessGeneratedCharacterDataCommand(
            self._playthrough_name,
            character_data,
            place_character_at_current_place,
            self._store_generated_character_command_factory,
            self._generate_character_image_command_factory,
            self._place_character_at_place_command_factory,
        )
