from src.base.required_string import RequiredString
from src.characters.factories.generate_character_generation_guidelines_algorithm_factory import (
    GenerateCharacterGenerationGuidelinesAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.movements.commands.visit_place_command import VisitPlaceCommand


class VisitPlaceCommandFactory:

    def __init__(
        self,
        playthrough_name: RequiredString,
        generate_character_generation_guidelines_algorithm_factory: GenerateCharacterGenerationGuidelinesAlgorithmFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
        place_manager_factory: PlaceManagerFactory,
    ):
        self._playthrough_name = playthrough_name
        self._generate_character_generation_guidelines_algorithm_factory = (
            generate_character_generation_guidelines_algorithm_factory
        )
        self._hierarchy_manager_factory = hierarchy_manager_factory
        self._place_manager_factory = place_manager_factory

    def create_visit_place_command(
        self, place_identifier: RequiredString
    ) -> VisitPlaceCommand:
        return VisitPlaceCommand(
            self._playthrough_name,
            place_identifier,
            self._generate_character_generation_guidelines_algorithm_factory,
            self._hierarchy_manager_factory,
            self._place_manager_factory,
        )
