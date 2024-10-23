from pydantic import BaseModel

from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.strategies import ProduceToolResponseStrategy
from src.prompting.factories.llm_content_provider_factory import (
    LlmContentProviderFactory,
)


class BaseModelProduceToolResponseStrategy(ProduceToolResponseStrategy):

    def __init__(
        self,
        llm_content_provider_factory: LlmContentProviderFactory,
    ):
        self._llm_content_provider_factory = llm_content_provider_factory

    def produce_tool_response(
        self, system_content: str, user_content: str
    ) -> BaseModel:
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

        product = llm_content_product.get()

        if not isinstance(product, BaseModel):
            raise TypeError(
                f"This strategy only handles base models, not the type '{type(product)}'."
            )

        return product
