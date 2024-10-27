from pathlib import Path

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.enums import ConceptType
from src.concepts.factories.dilemmas_factory import (
    DilemmasFactory,
)
from src.concepts.products.dilemmas_product import (
    DilemmasProduct,
)


class GenerateDilemmasAlgorithm(BaseConceptAlgorithm[DilemmasProduct, DilemmasFactory]):
    def get_save_file_path(self) -> Path:
        return self._path_manager.get_concept_file_path(
            self._playthrough_name, ConceptType.DILEMMAS
        )
