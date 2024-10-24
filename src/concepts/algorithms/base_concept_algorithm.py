import logging
from typing import Generic, TypeVar, List, Optional

from src.base.validators import validate_non_empty_string
from src.concepts.models.dilemmas import Dilemmas
from src.concepts.models.goals import Goals
from src.concepts.models.plot_blueprint import PlotBlueprint
from src.concepts.models.plot_twists import PlotTwists
from src.concepts.models.scenarios import Scenarios
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)
TProduct = TypeVar("TProduct")
TFactory = TypeVar("TFactory")


class BaseConceptAlgorithm(Generic[TProduct, TFactory]):

    def __init__(
        self,
        playthrough_name: str,
        action_name: str,
        concept_factory: TFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(action_name, "action_name")

        self._playthrough_name = playthrough_name
        self._action_name = action_name
        self._concept_factory = concept_factory
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def do_algorithm(self) -> List[str]:
        if self._action_name.lower() == "plot_blueprints":
            product = self._concept_factory.generate_product(PlotBlueprint)
        elif self._action_name.lower() == "situations":
            product = self._concept_factory.generate_product(Scenarios)
        elif self._action_name.lower() == "dilemmas":
            product = self._concept_factory.generate_product(Dilemmas)
        elif self._action_name.lower() == "goals":
            product = self._concept_factory.generate_product(Goals)
        elif self._action_name.lower() == "plot_twists":
            product = self._concept_factory.generate_product(PlotTwists)
        else:
            raise NotImplementedError(
                f"BaseConceptAlgorithm doesn't handle action name '{self._action_name}'."
            )

        if not product.is_valid():
            error_message = f"Failed to generate product from {self._concept_factory.__class__.__name__}. Error: {product.get_error()}"
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
        file_path = self.get_save_file_path()
        curated_items = []
        for item in items:
            if not item:
                raise ValueError(
                    f"Received a list with at least an invalid item: {items}"
                )
            curated_items.append(item)
        content = "\n".join(filter(None, [item for item in curated_items]))
        self._filesystem_manager.append_to_file(file_path, content)
        logger.info(f"Saved generated items to '{file_path}'.")

    def get_save_file_path(self) -> str:
        raise NotImplementedError("Subclasses must implement get_save_file_path.")
