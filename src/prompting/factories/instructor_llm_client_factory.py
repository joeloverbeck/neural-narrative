from typing import Optional, Type

import instructor
from instructor import Mode
from openai import OpenAI
from pydantic import BaseModel

from src.base.constants import OPENROUTER_API_URL
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import LlmClientFactory
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.instructor_llm_client import InstructorLlmClient


class InstructorLlmClientFactory(LlmClientFactory):
    def __init__(
        self,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def create_llm_client(self, response_model: Type[BaseModel]) -> LlmClient:
        return InstructorLlmClient(
            instructor.from_openai(
                OpenAI(
                    api_key=self._filesystem_manager.load_openrouter_secret_key(),
                    base_url=OPENROUTER_API_URL,
                ),
                mode=Mode.JSON,
            ),
            response_model,
        )
