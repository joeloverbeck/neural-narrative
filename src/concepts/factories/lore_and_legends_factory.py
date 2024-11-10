from typing import Optional

from pydantic import BaseModel

from src.base.products.texts_product import TextsProduct
from src.concepts.algorithms.get_concepts_prompt_data_algorithm import (
    GetConceptsPromptDataAlgorithm,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.filesystem.path_manager import PathManager
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)


class LoreAndLegendsFactory(BaseConceptFactory):

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
            prompt_file=path_manager.get_lore_and_legends_generation_prompt_path(),
            user_content="Generate a fascinating piece of world lore or legends that could stem from the provided information, as per the above instructions.",
            path_manager=path_manager,
        )

    def create_product_from_base_model(self, response_model: BaseModel):
        return TextsProduct([response_model.lore_or_legend], is_valid=True)
