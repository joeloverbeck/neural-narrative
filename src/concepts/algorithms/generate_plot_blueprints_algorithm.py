# src/concepts/algorithms/generate_plot_blueprints_algorithm.py

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.concepts.products.plot_blueprints_product import PlotBlueprintsProduct


class GeneratePlotBlueprintsAlgorithm(
    BaseConceptAlgorithm[PlotBlueprintsProduct, PlotBlueprintsFactory]
):
    def get_save_file_path(self) -> str:
        return self._filesystem_manager.get_file_path_to_plot_blueprints(
            self._playthrough_name
        )
