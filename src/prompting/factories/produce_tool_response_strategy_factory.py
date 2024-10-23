from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.llm_content_provider_factory import (
    LlmContentProviderFactory,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)
from src.prompting.strategies.concrete_produce_tool_response_strategy import (
    ConcreteProduceToolResponseStrategy,
)


class ProduceToolResponseStrategyFactory:

    def __init__(
        self,
        llm_content_provider_factory: LlmContentProviderFactory,
        tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory,
    ):
        self._llm_content_provider_factory = llm_content_provider_factory
        self._tool_response_parsing_provider_factory = (
            tool_response_parsing_provider_factory
        )

    def create_produce_tool_response_strategy(self) -> ProduceToolResponseStrategy:
        return ConcreteProduceToolResponseStrategy(
            self._llm_content_provider_factory,
            self._tool_response_parsing_provider_factory,
        )
