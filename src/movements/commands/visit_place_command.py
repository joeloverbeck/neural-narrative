from typing import Optional

from src.base.abstracts.command import Command
from src.base.constants import TIME_ADVANCED_DUE_TO_EXITING_LOCATION
from src.base.playthrough_manager import PlaythroughManager
from src.characters.character_guidelines_manager import CharacterGuidelinesManager
from src.characters.factories.generate_character_generation_guidelines_algorithm_factory import (
    GenerateCharacterGenerationGuidelinesAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.time.time_manager import TimeManager


class VisitPlaceCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        place_identifier: str,
        generate_character_generation_guidelines_algorithm_factory: GenerateCharacterGenerationGuidelinesAlgorithmFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
        place_manager_factory: PlaceManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        time_manager: Optional[TimeManager] = None,
        character_guidelines_manager: Optional[CharacterGuidelinesManager] = None,
    ):
        self._place_identifier = place_identifier
        (self._generate_character_generation_guidelines_algorithm_factory) = (
            generate_character_generation_guidelines_algorithm_factory
        )
        self._hierarchy_manager_factory = hierarchy_manager_factory
        self._place_manager_factory = place_manager_factory
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._time_manager = time_manager or TimeManager(playthrough_name)
        self._character_guidelines_manager = (
            character_guidelines_manager or CharacterGuidelinesManager()
        )

    def _handle_place_is_not_visited(self):
        story_universe_name = self._playthrough_manager.get_story_universe_template()
        places_templates_parameter = self._hierarchy_manager_factory.create_hierarchy_manager().fill_places_templates_parameter(
            self._place_identifier
        )
        if not self._character_guidelines_manager.guidelines_exist(
            story_universe_name,
            places_templates_parameter.get_world_template(),
            places_templates_parameter.get_region_template(),
            places_templates_parameter.get_area_template(),
            places_templates_parameter.get_location_template(),
        ):
            self._generate_character_generation_guidelines_algorithm_factory.create_algorithm(
                self._place_identifier
            ).do_algorithm()
        self._place_manager_factory.create_place_manager().set_as_visited(
            self._place_identifier
        )

    def execute(self) -> None:
        self._playthrough_manager.update_current_place(self._place_identifier)

        if not self._place_manager_factory.create_place_manager().is_visited(
            self._place_identifier
        ):
            self._handle_place_is_not_visited()
        self._time_manager.advance_time(TIME_ADVANCED_DUE_TO_EXITING_LOCATION)
