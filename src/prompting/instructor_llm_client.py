import logging
from typing import Type, Optional

from instructor import Instructor
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)
from pydantic import BaseModel

from src.dialogues.messages_to_llm import MessagesToLlm
from src.filesystem.config_loader import ConfigLoader
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.products.instructor_ai_completion_product import (
    InstructorAiCompletionProduct,
)

logger = logging.getLogger(__name__)


class InstructorLlmClient(LlmClient):
    def __init__(
        self,
        client: Instructor,
        response_model: Type[BaseModel],
        config_loader: Optional[ConfigLoader] = None,
    ):
        if not client:
            raise ValueError("client must not be empty.")

        # Unless you supress logging messages lower than WARNING, the log file will get swamped with messages.
        logging.getLogger("httpx").setLevel(logging.WARNING)

        self._client = client
        self._response_model = response_model

        self._config_loader = config_loader or ConfigLoader()

    def generate_completion(
        self, model: str, messages_to_llm: MessagesToLlm, temperature=1.0, top_p=1.0
    ) -> AiCompletionProduct:
        # Convert messages_to_llm.get() to the expected message types
        messages = [
            (
                ChatCompletionUserMessageParam(**message)
                if message["role"] == "user"
                else ChatCompletionSystemMessageParam(**message)
            )
            for message in messages_to_llm.get()
        ]

        model_result = self._client.chat.completions.create(
            model=model,
            max_retries=self._config_loader.get_max_retries(),
            messages=messages,
            response_model=self._response_model,
        )

        return InstructorAiCompletionProduct(model_result)

    def generate_image(self, prompt: str) -> str:
        raise NotImplemented(
            "This LLM client is not meant to be used to generate images."
        )
