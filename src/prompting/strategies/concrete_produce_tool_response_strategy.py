from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.providers.concrete_llm_content_provider import ConcreteLlmContentProvider
from src.prompting.providers.concrete_tool_response_parsing_provider import ConcreteToolResponseParsingProvider


class ConcreteProduceToolResponseStrategy(ProduceToolResponseStrategy):

    def __init__(self, llm_client: LlmClient, model: str):
        assert llm_client
        assert model

        self._llm_client = llm_client
        self._model = model

    def produce_tool_response(self, system_content: str, user_content: str) -> dict:
        messages_to_llm = MessagesToLlm()

        messages_to_llm.add_message("system", system_content)
        messages_to_llm.add_message("user", user_content)
        
        llm_content_product = ConcreteLlmContentProvider(self._model, messages_to_llm,
                                                         self._llm_client).generate_content()

        if not llm_content_product.is_valid():
            raise ValueError(f"Failed to receive content from LLM: {llm_content_product.get_error()}")

        tool_response_parsing_product = ConcreteToolResponseParsingProvider(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Failed to parse the response from the LLM, intending to get a tool call: {tool_response_parsing_product.get_error()}")

        return tool_response_parsing_product.get()
