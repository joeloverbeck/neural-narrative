from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.scenarios_factory import (
    ScenariosFactory,
)
from src.concepts.products.scenarios_product import (
    ScenariosProduct,
)


class GenerateInterestingSituationsAlgorithm(
    BaseConceptAlgorithm[ScenariosProduct, ScenariosFactory]
):

    def get_save_file_path(self) -> str:
        return self._filesystem_manager.get_file_path_to_interesting_situations(
            self._playthrough_name
        )
