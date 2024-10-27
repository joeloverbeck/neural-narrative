from pathlib import Path

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.enums import ConceptType
from src.concepts.factories.scenarios_factory import (
    ScenariosFactory,
)
from src.concepts.products.scenarios_product import (
    ScenariosProduct,
)


class GenerateScenariosAlgorithm(
    BaseConceptAlgorithm[ScenariosProduct, ScenariosFactory]
):

    def get_save_file_path(self) -> Path:
        return self._path_manager.get_concept_file_path(
            self._playthrough_name, ConceptType.SCENARIOS
        )
