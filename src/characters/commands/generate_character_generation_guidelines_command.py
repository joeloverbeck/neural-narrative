import logging

from src.abstracts.command import Command
from src.characters.characters_manager import CharactersManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.character_generation_guidelines_factory import (
    CharacterGenerationGuidelinesFactory,
)

logger = logging.getLogger(__name__)


class GenerateCharacterGenerationGuidelinesCommand(Command):

    def __init__(
            self,
            playthrough_name: str,
            place_identifier: str,
            character_generation_guidelines_factory: CharacterGenerationGuidelinesFactory,
            map_manager: MapManager = None,
            playthrough_manager: PlaythroughManager = None,
            characters_manager: CharactersManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._place_identifier = place_identifier
        self._character_generation_guidelines_factory = (
            character_generation_guidelines_factory
        )

        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        places_templates_parameter = self._map_manager.fill_places_templates_parameter(
            self._place_identifier
        )

        world_name = self._playthrough_manager.get_world_template()

        key = self._characters_manager.create_key_for_character_generation_guidelines(
            world_name,
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            places_templates_parameter.get_location_template(),
        )

        if self._characters_manager.are_there_character_generation_guidelines_for_place(
                world_name,
                places_templates_parameter.get_region_template(),
                places_templates_parameter.get_area_template(),
                places_templates_parameter.get_location_template(),
        ):
            logger.info(
                f"There were already character generation guidelines created for {key}."
            )
            return

        result = (
            self._character_generation_guidelines_factory.generate_character_generation_guidelines()
        )

        if not result.is_valid():
            raise ValueError(
                f"There was an error when creating the guidelines for character generation: {result.get_error()}"
            )

        # We have the guidelines, and now we ought to store them.
        self._characters_manager.save_character_generation_guidelines(
            world_name,
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            result.get(),
            places_templates_parameter.get_location_template(),
        )

        logger.info(f"Generated character generation guidelines for key '{key}'.")
