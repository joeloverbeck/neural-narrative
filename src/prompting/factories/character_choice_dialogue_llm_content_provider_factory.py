from src.dialogues.abstracts.factory_products import InitialPromptingMessagesProduct
from src.prompting.abstracts.abstract_factories import LlmContentProvider
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.providers.concrete_llm_content_provider import (
    ConcreteLlmContentProvider,
)


class CharacterChoiceDialogueLlmContentProviderFactory:

    def __init__(self, llm_client: LlmClient, model: str):
        self._llm_client = llm_client
        self._model = model

    def create_llm_content_provider_factory(
        self,
        character_choice_dialogue_initial_prompting_messages_product: InitialPromptingMessagesProduct,
    ) -> LlmContentProvider:
        return ConcreteLlmContentProvider(
            model=self._model,
            messages_to_llm=character_choice_dialogue_initial_prompting_messages_product.get(),
            llm_client=self._llm_client,
        )
