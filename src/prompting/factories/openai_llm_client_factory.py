from typing import Type, Optional

from openai import OpenAI
from pydantic import BaseModel

from src.filesystem.config_loader import ConfigLoader
from src.prompting.abstracts.abstract_factories import LlmClientFactory
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.llm import Llm
from src.prompting.open_ai_llm_client import OpenAiLlmClient


class OpenAILlmClientFactory(LlmClientFactory):

    def __init__(self, config_loader: Optional[ConfigLoader] = None):
        self._config_loader = config_loader or ConfigLoader()

    def create_llm_client(
        self,
        _llm: Optional[Llm] = None,
        _response_model: Optional[Type[BaseModel]] = None,
    ) -> LlmClient:
        return OpenAiLlmClient(
            OpenAI(
                api_key=self._config_loader.load_openai_secret_key(),
                project=self._config_loader.load_openai_project_key(),
            )
        )
