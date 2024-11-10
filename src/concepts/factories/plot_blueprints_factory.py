import logging
from typing import Optional

from pydantic import BaseModel

from src.concepts.algorithms.get_concepts_prompt_data_algorithm import (
    GetConceptsPromptDataAlgorithm,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.plot_blueprints_product import PlotBlueprintsProduct
from src.filesystem.path_manager import PathManager
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)

logger = logging.getLogger(__name__)


class PlotBlueprintsFactory(BaseConceptFactory):

    def __init__(
        self,
        get_concepts_prompt_data_algorithm: GetConceptsPromptDataAlgorithm,
        produce_tool_response_strategy_factory: BaseModelProduceToolResponseStrategyFactory,
        path_manager: Optional[PathManager] = None,
    ):
        path_manager = path_manager or PathManager()

        super().__init__(
            get_concepts_prompt_data_algorithm,
            produce_tool_response_strategy_factory,
            prompt_file=path_manager.get_plot_blueprints_generation_prompt_path(),
            user_content="Generate a magnificent plot blueprint for a full story. Follow the provided instructions.",
            path_manager=path_manager,
        )

    def create_product_from_base_model(self, response_model: BaseModel):
        plot_blueprint = (
            str(response_model.plot_blueprint).replace("\n\n", " ").replace("\n", " ")
        )
        if not plot_blueprint.strip():
            return PlotBlueprintsProduct(
                None,
                is_valid=False,
                error="The LLM failed to produce a plot blueprint.",
            )
        return PlotBlueprintsProduct([plot_blueprint], is_valid=True)
