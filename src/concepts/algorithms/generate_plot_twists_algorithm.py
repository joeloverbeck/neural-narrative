from pathlib import Path

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.enums import ConceptType
from src.concepts.factories.plot_twists_factory import PlotTwistsFactory
from src.concepts.products.plot_twists_product import PlotTwistsProduct


class GeneratePlotTwistsAlgorithm(
    BaseConceptAlgorithm[PlotTwistsProduct, PlotTwistsFactory]
):

    def get_save_file_path(self) -> Path:
        return self._path_manager.get_concept_file_path(
            self._playthrough_name, ConceptType.PLOT_TWISTS
        )
