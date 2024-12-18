from src.characters.composers.character_generation_guidelines_provider_factory_composer import (
    CharacterGenerationGuidelinesProviderFactoryComposer,
)
from src.characters.factories.generate_character_generation_guidelines_algorithm_factory import (
    GenerateCharacterGenerationGuidelinesAlgorithmFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.factories.visit_place_command_factory import VisitPlaceCommandFactory
from src.movements.factories.process_first_visit_to_place_command_factory import (
    ProcessFirstVisitToPlaceCommandFactory,
)


class VisitPlaceCommandFactoryComposer:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def compose_factory(self) -> VisitPlaceCommandFactory:
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        character_generation_guidelines_provider_factory = (
            CharacterGenerationGuidelinesProviderFactoryComposer(
                self._playthrough_name
            ).compose_factory()
        )
        hierarchy_manager_factory = HierarchyManagerFactory(self._playthrough_name)

        generate_character_generation_guidelines_algorithm_factory = (
            GenerateCharacterGenerationGuidelinesAlgorithmFactory(
                self._playthrough_name,
                character_generation_guidelines_provider_factory,
                hierarchy_manager_factory,
            )
        )

        hierarchy_manager_factory = HierarchyManagerFactory(self._playthrough_name)

        process_first_visit_to_place_command_factory = (
            ProcessFirstVisitToPlaceCommandFactory(
                self._playthrough_name,
                generate_character_generation_guidelines_algorithm_factory,
                hierarchy_manager_factory,
                place_manager_factory,
            )
        )

        return VisitPlaceCommandFactory(
            self._playthrough_name,
            process_first_visit_to_place_command_factory,
            place_manager_factory,
        )
