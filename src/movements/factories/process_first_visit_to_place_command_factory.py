from src.base.validators import validate_non_empty_string
from src.characters.factories.generate_character_generation_guidelines_algorithm_factory import (
    GenerateCharacterGenerationGuidelinesAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.commands.process_first_visit_to_place_command import (
    ProcessFirstVisitToPlaceCommand,
)


class ProcessFirstVisitToPlaceCommandFactory:
    def __init__(
        self,
        playthrough_name: str,
        generate_character_generation_guidelines_algorithm_factory: GenerateCharacterGenerationGuidelinesAlgorithmFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
        place_manager_factory: PlaceManagerFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._generate_character_generation_guidelines_algorithm_factory = (
            generate_character_generation_guidelines_algorithm_factory
        )
        self._hierarchy_manager_factory = hierarchy_manager_factory
        self._place_manager_factory = place_manager_factory

    def create_command(
        self, map_entry_identifier: str
    ) -> ProcessFirstVisitToPlaceCommand:
        return ProcessFirstVisitToPlaceCommand(
            self._playthrough_name,
            map_entry_identifier,
            self._generate_character_generation_guidelines_algorithm_factory,
            self._hierarchy_manager_factory,
            self._place_manager_factory,
        )
