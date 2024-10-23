import logging
from typing import Type

from instructor import Instructor
from pydantic import BaseModel

from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.products.instructor_ai_completion_product import (
    InstructorAiCompletionProduct,
)

logger = logging.getLogger(__name__)


class InstructorLlmClient(LlmClient):
    def __init__(self, client: Instructor, response_model: Type[BaseModel]):
        if not client:
            raise ValueError("client must not be empty.")

        # Unless you supress logging messages lower than WARNING, the log file will get swamped with messages.
        logging.getLogger("httpx").setLevel(logging.WARNING)

        self._client = client
        self._response_model = response_model

    def generate_completion(
        self, model: str, messages_to_llm: MessagesToLlm, temperature=1.0, top_p=1.0
    ) -> AiCompletionProduct:
        model_result = self._client.chat.completions.create(
            response_model=self._response_model,
            model=model,
            messages=messages_to_llm.get(),
        )

        return InstructorAiCompletionProduct(model_result)

    def generate_image(self, prompt: str) -> str:
        raise NotImplemented(
            "This LLM client is not meant to be used to generate images."
        )
