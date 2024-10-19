from openai import OpenAI

from src.base.constants import OPENROUTER_API_URL
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import LlmClientFactory
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.open_ai_llm_client import OpenAiLlmClient


class OpenRouterLlmClientFactory(LlmClientFactory):
    def create_llm_client(self) -> LlmClient:
        filesystem_manager = FilesystemManager()

        return OpenAiLlmClient(OpenAI(
            base_url=OPENROUTER_API_URL,
            api_key=filesystem_manager.load_openrouter_secret_key()
        ))
