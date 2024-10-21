from src.base.required_string import RequiredString
from src.dialogues.abstracts.abstract_factories import DialogueSummaryProvider
from src.dialogues.providers.concrete_dialogue_summary_provider import (
    ConcreteDialogueSummaryProvider,
)
from src.dialogues.transcription import Transcription
from src.prompting.abstracts.llm_client import LlmClient


class DialogueSummaryProviderFactory:
    def __init__(self, llm_client: LlmClient, model: RequiredString):
        if not model:
            raise ValueError("model can't be empty.")

        self._llm_client = llm_client
        self._model = model

    def create_dialogue_summary_provider(
            self, transcription: Transcription
    ) -> DialogueSummaryProvider:
        return ConcreteDialogueSummaryProvider(
            self._llm_client, self._model, transcription
        )
