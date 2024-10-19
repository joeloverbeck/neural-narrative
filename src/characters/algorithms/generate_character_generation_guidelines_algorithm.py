import logging
from typing import Optional, cast

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.factories.character_generation_guidelines_factory import (
    CharacterGenerationGuidelinesFactory,
)
from src.characters.products.character_generation_guidelines_product import (
    CharacterGenerationGuidelinesProduct,
)
from src.maps.map_manager import MapManager

logger = logging.getLogger(__name__)


class GenerateCharacterGenerationGuidelinesAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        place_identifier: str,
        character_generation_guidelines_factory: CharacterGenerationGuidelinesFactory,
        map_manager: Optional[MapManager] = None,
        playthrough_manager: Optional[PlaythroughManager] = None,
        character_guidelines_manager: Optional[CharacterGuidelinesManager] = None,
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
        self._character_guidelines_manager = (
            character_guidelines_manager or CharacterGuidelinesManager()
        )

    def do_algorithm(self) -> CharacterGenerationGuidelinesProduct:
        places_templates_parameter = self._map_manager.fill_places_templates_parameter(
            self._place_identifier
        )

        world_name = self._playthrough_manager.get_world_template()

        key = self._character_guidelines_manager.create_key(
            world_name,
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            places_templates_parameter.get_location_template(),
        )

        result = cast(
            CharacterGenerationGuidelinesProduct,
            self._character_generation_guidelines_factory.generate_product(),
        )

        if not result.is_valid():
            raise ValueError(
                f"There was an error when creating the guidelines for character generation: {result.get_error()}"
            )

        # We have the guidelines, and now we ought to store them.
        self._character_guidelines_manager.save_guidelines(
            world_name,
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            result.get(),
            places_templates_parameter.get_location_template(),
        )

        logger.info(f"Generated character generation guidelines for key '{key}'.")

        return result
