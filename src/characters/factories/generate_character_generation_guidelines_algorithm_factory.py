from src.characters.algorithms.generate_character_generation_guidelines_algorithm import (
    GenerateCharacterGenerationGuidelinesAlgorithm,
)
from src.characters.factories.character_generation_guidelines_provider_factory import (
    CharacterGenerationGuidelinesProviderFactory,
)
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory


class GenerateCharacterGenerationGuidelinesAlgorithmFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_generation_guidelines_provider_factory: CharacterGenerationGuidelinesProviderFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
    ):
        self._playthrough_name = playthrough_name
        self._character_generation_guidelines_provider_factory = (
            character_generation_guidelines_provider_factory
        )
        self._hierarchy_manager_factory = hierarchy_manager_factory

    def create_algorithm(
        self, place_identifier: str
    ) -> GenerateCharacterGenerationGuidelinesAlgorithm:
        return GenerateCharacterGenerationGuidelinesAlgorithm(
            self._playthrough_name,
            place_identifier,
            self._character_generation_guidelines_provider_factory,
            self._hierarchy_manager_factory,
        )
