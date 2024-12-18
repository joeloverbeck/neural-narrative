import logging
from typing import Optional, cast

from src.base.playthrough_manager import PlaythroughManager
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.factories.character_generation_guidelines_provider_factory import (
    CharacterGenerationGuidelinesProviderFactory,
)
from src.characters.models.character_guidelines import CharacterGuidelines
from src.characters.products.character_generation_guidelines_product import (
    CharacterGenerationGuidelinesProduct,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory

logger = logging.getLogger(__name__)


class GenerateCharacterGenerationGuidelinesAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        place_identifier: str,
        character_generation_guidelines_provider_factory: CharacterGenerationGuidelinesProviderFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        character_guidelines_manager: Optional[CharacterGuidelinesManager] = None,
    ):
        self._place_identifier = place_identifier
        self._character_generation_guidelines_provider_factory = (
            character_generation_guidelines_provider_factory
        )
        self._hierarchy_manager_factory = hierarchy_manager_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._character_guidelines_manager = (
            character_guidelines_manager or CharacterGuidelinesManager()
        )

    def do_algorithm(self) -> CharacterGenerationGuidelinesProduct:
        places_templates_parameter = self._hierarchy_manager_factory.create_hierarchy_manager().fill_places_templates_parameter(
            self._place_identifier
        )
        story_universe_name = self._playthrough_manager.get_story_universe_template()
        key = self._character_guidelines_manager.create_key(
            story_universe_name,
            places_templates_parameter.get_world_template(),
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            places_templates_parameter.get_location_template(),
        )
        result = cast(
            CharacterGenerationGuidelinesProduct,
            self._character_generation_guidelines_provider_factory.create_provider().generate_product(
                CharacterGuidelines
            ),
        )
        if not result.is_valid():
            raise ValueError(
                f"There was an error when creating the guidelines for character generation: {result.get_error()}"
            )
        self._character_guidelines_manager.save_guidelines(
            story_universe_name,
            places_templates_parameter.get_world_template(),
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            result.get(),
            places_templates_parameter.get_location_template(),
        )
        logger.info(f"Generated character generation guidelines for key '{key}'.")
        return result
