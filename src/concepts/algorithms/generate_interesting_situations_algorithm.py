from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.interesting_situations_factory import (
    InterestingSituationsFactory,
)
from src.concepts.products.interesting_situations_product import (
    InterestingSituationsProduct,
)


class GenerateInterestingSituationsAlgorithm(
    BaseConceptAlgorithm[InterestingSituationsProduct, InterestingSituationsFactory]
):

    def get_save_file_path(self) -> str:
        return self._filesystem_manager.get_file_path_to_interesting_situations(
            self._playthrough_name
        )
