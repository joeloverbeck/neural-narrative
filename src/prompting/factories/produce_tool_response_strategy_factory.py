from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.llm_content_provider_factory import LlmContentProviderFactory
from src.prompting.factories.tool_response_parsing_provider_factory import ToolResponseParsingProviderFactory
from src.prompting.strategies.concrete_produce_tool_response_strategy import ConcreteProduceToolResponseStrategy


class ProduceToolResponseStrategyFactory:
    def __init__(self, llm_client: LlmClient, model: str):
        if not model:
            raise ValueError("model can't be empty.")

        self._llm_client = llm_client
        self._model = model

    def create_produce_tool_response_strategy(self) -> ProduceToolResponseStrategy:
        llm_content_provider_factory = LlmContentProviderFactory(self._llm_client, model=self._model)

        tool_response_parsing_provider_factory = ToolResponseParsingProviderFactory()

        return ConcreteProduceToolResponseStrategy(llm_content_provider_factory,
                                                   tool_response_parsing_provider_factory)
