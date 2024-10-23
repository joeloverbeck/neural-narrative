from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.llm_content_provider_factory import (
    LlmContentProviderFactory,
)
from src.prompting.strategies.base_model_produce_tool_response_strategy import (
    BaseModelProduceToolResponseStrategy,
)


class BaseModelProduceToolResponseStrategyFactory(ProduceToolResponseStrategyFactory):

    def __init__(
        self,
        llm_content_provider_factory: LlmContentProviderFactory,
    ):
        self._llm_content_provider_factory = llm_content_provider_factory

    def create_produce_tool_response_strategy(self) -> ProduceToolResponseStrategy:
        return BaseModelProduceToolResponseStrategy(
            self._llm_content_provider_factory,
        )
