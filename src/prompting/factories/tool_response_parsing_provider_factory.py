from src.prompting.abstracts.abstract_factories import ToolResponseParsingProvider
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.providers.concrete_tool_response_parsing_provider import ConcreteToolResponseParsingProvider


class ToolResponseParsingProviderFactory:
    @staticmethod
    def create_tool_response_parsing_provider(llm_content_product: LlmContentProduct) -> ToolResponseParsingProvider:
        return ConcreteToolResponseParsingProvider(
            llm_content_product.get())
