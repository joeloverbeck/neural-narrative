from pathlib import Path

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.enums import ConceptType
from src.concepts.factories.goals_factory import GoalsFactory
from src.concepts.products.goals_product import GoalsProduct


class GenerateGoalsAlgorithm(BaseConceptAlgorithm[GoalsProduct, GoalsFactory]):

    def get_save_file_path(self) -> Path:
        return self._path_manager.get_concept_file_path(
            self._playthrough_name, ConceptType.GOALS
        )
