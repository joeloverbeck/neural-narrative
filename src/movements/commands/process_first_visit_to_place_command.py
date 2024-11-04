import logging
from typing import Optional

from src.base.abstracts.command import Command
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.factories.generate_character_generation_guidelines_algorithm_factory import (
    GenerateCharacterGenerationGuidelinesAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory

logger = logging.getLogger(__name__)


class ProcessFirstVisitToPlaceCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        map_entry_identifier: str,
        generate_character_generation_guidelines_algorithm_factory: GenerateCharacterGenerationGuidelinesAlgorithmFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
        place_manager_factory: PlaceManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        character_guidelines_manager: Optional[CharacterGuidelinesManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(map_entry_identifier, "map_entry_identifier")

        self._map_entry_identifier = map_entry_identifier
        self._generate_character_generation_guidelines_algorithm_factory = (
            generate_character_generation_guidelines_algorithm_factory
        )
        self._hierarchy_manager_factory = hierarchy_manager_factory
        self._place_manager_factory = place_manager_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._character_guidelines_manager = (
            character_guidelines_manager or CharacterGuidelinesManager()
        )

    def execute(self) -> None:
        place_manager = self._place_manager_factory.create_place_manager()

        if place_manager.get_current_place_type() == TemplateType.ROOM:
            # Guidelines shouldn't be created for rooms, and they don't have the notion of "visited" either.
            logger.warning(
                "Was going to process the first visit for a room. This command shouldn't be executed for rooms."
            )
            return

        places_templates_parameter = self._hierarchy_manager_factory.create_hierarchy_manager().fill_places_templates_parameter(
            self._map_entry_identifier
        )

        story_universe_name = self._playthrough_manager.get_story_universe_template()

        if not self._character_guidelines_manager.guidelines_exist(
            story_universe_name,
            places_templates_parameter.get_world_template(),
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            places_templates_parameter.get_location_template(),
        ):
            self._generate_character_generation_guidelines_algorithm_factory.create_algorithm(
                self._map_entry_identifier
            ).do_algorithm()

        place_manager.set_as_visited(self._map_entry_identifier)
