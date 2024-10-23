from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.abstract_factories import LlmContentProvider
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.providers.concrete_llm_content_provider import (
    ConcreteLlmContentProvider,
)


class LlmContentProviderFactory:

    def __init__(self, llm_client: LlmClient, model: str):
        self._llm_client = llm_client
        self._model = model

    def create_llm_content_provider(
        self, messages_to_llm: MessagesToLlm
    ) -> LlmContentProvider:
        return ConcreteLlmContentProvider(
            self._model, messages_to_llm, self._llm_client
        )
