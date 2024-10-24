from typing import Type, Optional

from openai import OpenAI
from pydantic import BaseModel

from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import LlmClientFactory
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.open_ai_llm_client import OpenAiLlmClient


class OpenAILlmClientFactory(LlmClientFactory):

    def create_llm_client(
        self, _response_model: Optional[Type[BaseModel]] = None
    ) -> LlmClient:
        filesystem_manager = FilesystemManager()
        return OpenAiLlmClient(
            OpenAI(
                api_key=filesystem_manager.load_openai_secret_key(),
                project=filesystem_manager.load_openai_project_key(),
            )
        )
