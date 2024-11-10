from typing import Optional

from pydantic import BaseModel

from src.concepts.algorithms.get_concepts_prompt_data_algorithm import (
    GetConceptsPromptDataAlgorithm,
)
from src.concepts.factories.base_concept_factory import BaseConceptFactory
from src.concepts.products.scenarios_product import (
    ScenariosProduct,
)
from src.filesystem.path_manager import PathManager
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)


class ScenariosFactory(BaseConceptFactory):

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
            prompt_file=path_manager.get_scenarios_generation_prompt_path(),
            user_content="Write three very interesting and intriguing scenarios that could stem from the information provided, as per the above instructions.",
            path_manager=path_manager,
        )

    def create_product_from_base_model(self, response_model: BaseModel):
        return ScenariosProduct(response_model.scenarios, is_valid=True)
