from typing import Optional

from openai import OpenAI

from src.base.constants import OPENROUTER_API_URL
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import LlmClientFactory
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.open_ai_llm_client import OpenAiLlmClient


class OpenRouterLlmClientFactory(LlmClientFactory):
    def __init__(self, filesystem_manager: Optional[FilesystemManager] = None):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def create_llm_client(self) -> LlmClient:
        return OpenAiLlmClient(
            OpenAI(
                api_key=self._filesystem_manager.load_openrouter_secret_key(),
                base_url=OPENROUTER_API_URL,
            )
        )
