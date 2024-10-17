# src/concepts/algorithms/generate_goals_algorithm.py

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.goals_factory import GoalsFactory
from src.concepts.products.goals_product import GoalsProduct


class GenerateGoalsAlgorithm(BaseConceptAlgorithm[GoalsProduct, GoalsFactory]):
    def get_save_file_path(self) -> str:
        return self._filesystem_manager.get_file_path_to_goals(self._playthrough_name)
