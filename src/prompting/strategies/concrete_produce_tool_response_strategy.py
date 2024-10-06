from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.llm_content_provider_factory import (
    LlmContentProviderFactory,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)


class ConcreteProduceToolResponseStrategy(ProduceToolResponseStrategy):

    def __init__(
        self,
        llm_content_provider_factory: LlmContentProviderFactory,
        tool_response_parsing_provider_factory: ToolResponseParsingProviderFactory,
    ):
        self._llm_content_provider_factory = llm_content_provider_factory
        self._tool_response_parsing_provider_factory = (
            tool_response_parsing_provider_factory
        )

    def produce_tool_response(self, system_content: str, user_content: str) -> dict:
        messages_to_llm = MessagesToLlm()

        messages_to_llm.add_message("system", system_content)
        messages_to_llm.add_message("user", user_content)

        llm_content_product = (
            self._llm_content_provider_factory.create_llm_content_provider(
                messages_to_llm
            ).generate_content()
        )

        if not llm_content_product.is_valid():
            raise ValueError(
                f"Failed to receive content from LLM: {llm_content_product.get_error()}"
            )

        tool_response_parsing_product = self._tool_response_parsing_provider_factory.create_tool_response_parsing_provider(
            llm_content_product
        ).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            raise ValueError(
                f"Failed to parse the response from the LLM, intending to get a tool call: {tool_response_parsing_product.get_error()}"
            )

        return tool_response_parsing_product.get()
