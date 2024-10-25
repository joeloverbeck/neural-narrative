import logging
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
from src.prompting.llm import Llm

logger = logging.getLogger(__name__)


class InstructorLlmClientFactory(LlmClientFactory):
    def __init__(
        self,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def create_llm_client(self, llm: Llm, response_model: Type[BaseModel]) -> LlmClient:
        # Note: Mode.TOOLS doesn't work for some reason: it raises a NoneType exception.
        # The structure is done if in the future I want to delve into why this isn't working.
        mode = Mode.JSON if llm.supports_tools() else Mode.JSON

        return InstructorLlmClient(
            instructor.from_openai(
                OpenAI(
                    api_key=self._filesystem_manager.load_openrouter_secret_key(),
                    base_url=OPENROUTER_API_URL,
                ),
                mode=mode,
            ),
            response_model,
        )
