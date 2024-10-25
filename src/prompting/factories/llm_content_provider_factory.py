from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.abstract_factories import (
    LlmContentProvider,
    LlmClientFactory,
)
from src.prompting.llm import Llm
from src.prompting.providers.concrete_llm_content_provider import (
    ConcreteLlmContentProvider,
)


class LlmContentProviderFactory:

    def __init__(self, llm_client_factory: LlmClientFactory, llm: Llm):
        self._llm_client_factory = llm_client_factory
        self._llm = llm

    def create_llm_content_provider(
        self, messages_to_llm: MessagesToLlm
    ) -> LlmContentProvider:
        return ConcreteLlmContentProvider(
            self._llm, messages_to_llm, self._llm_client_factory
        )
