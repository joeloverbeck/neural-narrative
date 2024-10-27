from pathlib import Path

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.enums import ConceptType
from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.concepts.products.plot_blueprints_product import PlotBlueprintsProduct


class GeneratePlotBlueprintsAlgorithm(
    BaseConceptAlgorithm[PlotBlueprintsProduct, PlotBlueprintsFactory]
):

    def get_save_file_path(self) -> Path:
        return self._path_manager.get_concept_file_path(
            self._playthrough_name, ConceptType.PLOT_BLUEPRINTS
        )
