from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.plot_twists_factory import PlotTwistsFactory
from src.concepts.products.plot_twists_product import PlotTwistsProduct


class GeneratePlotTwistsAlgorithm(
    BaseConceptAlgorithm[PlotTwistsProduct, PlotTwistsFactory]
):

    def get_save_file_path(self) -> str:
        return self._filesystem_manager.get_file_path_to_plot_twists(
            self._playthrough_name
        )
