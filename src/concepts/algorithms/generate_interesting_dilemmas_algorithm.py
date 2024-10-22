from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.interesting_dilemmas_factory import (
    InterestingDilemmasFactory,
)
from src.concepts.products.interesting_dilemmas_product import (
    InterestingDilemmasProduct,
)


class GenerateInterestingDilemmasAlgorithm(
    BaseConceptAlgorithm[InterestingDilemmasProduct, InterestingDilemmasFactory]
):

    def get_save_file_path(self) -> str:
        return self._filesystem_manager.get_file_path_to_interesting_dilemmas(
            self._playthrough_name
        )
