import logging
from typing import Generic, TypeVar, List, Optional, Dict, Type

from src.base.validators import validate_non_empty_string
from src.concepts.enums import ConceptType
from src.concepts.models.antagonist import Antagonist
from src.concepts.models.dilemmas import Dilemmas
from src.concepts.models.goals import Goals
from src.concepts.models.plot_blueprint import PlotBlueprint
from src.concepts.models.plot_twists import PlotTwists
from src.concepts.models.scenarios import Scenarios
from src.concepts.repositories.concepts_repository import ConceptsRepository

logger = logging.getLogger(__name__)
TProduct = TypeVar("TProduct")
TFactory = TypeVar("TFactory")


class BaseConceptAlgorithm(Generic[TProduct, TFactory]):
    ACTION_CLASS_MAPPING: Dict[str, Type] = {
        ConceptType.PLOT_BLUEPRINTS.value: PlotBlueprint,
        ConceptType.SCENARIOS.value: Scenarios,
        ConceptType.DILEMMAS.value: Dilemmas,
        ConceptType.GOALS.value: Goals,
        ConceptType.PLOT_TWISTS.value: PlotTwists,
        ConceptType.ANTAGONISTS.value: Antagonist,
    }

    def __init__(
        self,
        playthrough_name: str,
        action_name: str,
        concept_factory: TFactory,
        concepts_repository: Optional[ConceptsRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(action_name, "action_name")

        self._action_name = action_name.lower()
        self._concept_factory = concept_factory
        self._concepts_repository = concepts_repository or ConceptsRepository(
            playthrough_name
        )

    def do_algorithm(self) -> List[str]:
        product_class = self.ACTION_CLASS_MAPPING.get(self._action_name)

        if not product_class:
            raise NotImplementedError(
                f"BaseConceptAlgorithm doesn't handle action name '{self._action_name}'."
            )

        product = self._concept_factory.generate_product(product_class)

        if not product.is_valid():
            error_message = (
                f"Failed to generate product from {self._concept_factory.__class__.__name__}. "
                f"Error: {product.get_error()}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

        generated_items = product.get()

        if not generated_items:
            raise ValueError(
                f"No items were generated by {self._concept_factory.__class__.__name__}."
            )

        self.save_generated_items(generated_items)

        return generated_items

    def save_generated_items(self, items: List[str]):
        if not items:
            raise ValueError("There weren't items to save.")

        self._concepts_repository.add_concepts(self._action_name, items)
