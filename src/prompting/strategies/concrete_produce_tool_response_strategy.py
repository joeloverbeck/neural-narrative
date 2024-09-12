from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.concrete_llm_content_factory import ConcreteLlmContentFactory
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory


class ConcreteProduceToolResponseStrategy(ProduceToolResponseStrategy):

    def __init__(self, llm_client: LlmClient, model: str):
        assert llm_client
        assert model

        self._llm_client = llm_client
        self._model = model

    def produce_tool_response(self, system_content: str, user_content: str) -> dict:
        llm_content_product = ConcreteLlmContentFactory(self._model, [
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": user_content,
            },
        ], self._llm_client).generate_content()

        if not llm_content_product.is_valid():
            raise ValueError(f"Failed to receive content from LLM: {llm_content_product.get_error()}")

        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Failed to parse the response from the LLM, intending to get a tool call: {tool_response_parsing_product.get_error()}")

        return tool_response_parsing_product.get()
