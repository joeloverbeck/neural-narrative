import logging
from typing import Type, Optional

from instructor import Instructor
from instructor.exceptions import InstructorRetryException
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)
from pydantic import BaseModel

from src.base.constants import (
    TOO_MANY_REQUESTS_ERROR_NUMBER,
    UNAUTHORIZED_ERROR_NUMBER,
    PAYMENT_REQUIRED,
    INVALID_SSL_CERTIFICATE,
    MAXIMUM_CONTENT_LENGTH_REACHED,
)
from src.base.enums import AiCompletionErrorType
from src.dialogues.messages_to_llm import MessagesToLlm
from src.filesystem.config_loader import ConfigLoader
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.llm import Llm
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
        self, model: Llm, messages_to_llm: MessagesToLlm
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

        try:
            model_result = self._client.chat.completions.create(
                model=model.get_name(),
                max_retries=self._config_loader.get_max_retries(),
                messages=messages,
                response_model=self._response_model,
                temperature=model.get_temperature(),
                top_p=model.get_top_p(),
            )
        except InstructorRetryException as e:
            logger.error(
                "Attempts: %s",
                e.n_attempts,
            )
            logger.error("Last completion:\n%s", e.last_completion)

            error_correlation = {
                TOO_MANY_REQUESTS_ERROR_NUMBER: AiCompletionErrorType.TOO_MANY_REQUESTS,
                UNAUTHORIZED_ERROR_NUMBER: AiCompletionErrorType.UNAUTHORIZED,
                PAYMENT_REQUIRED: AiCompletionErrorType.PAYMENT_REQUIRED,
                INVALID_SSL_CERTIFICATE: AiCompletionErrorType.INVALID_SSL_CERTIFICATE,
                MAXIMUM_CONTENT_LENGTH_REACHED: AiCompletionErrorType.MAXIMUM_CONTENT_LENGTH_REACHED,
            }

            return InstructorAiCompletionProduct(
                None,
                is_valid=False,
                error=error_correlation.get(
                    e.last_completion["error"]["code"], AiCompletionErrorType.UNHANDLED
                ),
            )

        return InstructorAiCompletionProduct(model_result, is_valid=True)

    def generate_image(self, prompt: str) -> str:
        raise NotImplemented(
            "This LLM client is not meant to be used to generate images."
        )
