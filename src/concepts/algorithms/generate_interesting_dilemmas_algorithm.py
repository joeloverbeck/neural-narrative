from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.dilemmas_factory import (
    DilemmasFactory,
)
from src.concepts.products.interesting_dilemmas_product import (
    InterestingDilemmasProduct,
)


class GenerateInterestingDilemmasAlgorithm(
    BaseConceptAlgorithm[InterestingDilemmasProduct, DilemmasFactory]
):

    def get_save_file_path(self) -> str:
        return self._filesystem_manager.get_file_path_to_interesting_dilemmas(
            self._playthrough_name
        )
