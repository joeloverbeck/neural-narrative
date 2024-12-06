import logging
from typing import Type, Optional

from instructor import Instructor
from instructor.exceptions import InstructorRetryException
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
)
from pydantic import BaseModel
from pydantic.v1 import ValidationError

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

        # Hook into the exceptions of the client to log them.

        def log_exception(exception: Exception):
            print(f"An exception occurred: {str(exception)}")

        self._client.on("completion:error", log_exception)

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
                frequency_penalty=model.get_frequency_penalty(),
                presence_penalty=model.get_presence_penalty(),
            )
        except ValidationError as e:
            error = f"Validation error: {str(e)}"
            logger.error(error)

            return InstructorAiCompletionProduct(
                None,
                is_valid=False,
                error=error,
            )
        except InstructorRetryException as e:
            logger.error("InstructorRetryException raised. Error: %s", str(e))
            logger.error(
                "Attempts: %s",
                e.n_attempts,
            )

            message = e.last_completion.choices[0].message

            content = message.content or "No valid content."

            logger.error("Last content:\n%s", content)

            try:
                # If the content doesn't end with a closing brace, append one.
                if not content.endswith("}"):
                    content += "}"

                # Attempt to validate the JSON content against the response model.
                parsed_result = self._response_model.model_validate_json(content)

                # If successful, return a valid product early.
                return InstructorAiCompletionProduct(parsed_result, is_valid=True)
            except ValueError as parse_error:
                logger.error("Parsing corrected content failed: %s", str(parse_error))
                # If parsing still fails, continue with the existing error handling below.

                error_correlation = {
                    TOO_MANY_REQUESTS_ERROR_NUMBER: AiCompletionErrorType.TOO_MANY_REQUESTS,
                    UNAUTHORIZED_ERROR_NUMBER: AiCompletionErrorType.UNAUTHORIZED,
                    PAYMENT_REQUIRED: AiCompletionErrorType.PAYMENT_REQUIRED,
                    INVALID_SSL_CERTIFICATE: AiCompletionErrorType.INVALID_SSL_CERTIFICATE,
                    MAXIMUM_CONTENT_LENGTH_REACHED: AiCompletionErrorType.MAXIMUM_CONTENT_LENGTH_REACHED,
                }

                error = (
                    content
                    if not hasattr(e.last_completion, "error")
                    else error_correlation.get(
                        e.last_completion.error["code"], AiCompletionErrorType.UNHANDLED
                    )
                )

                return InstructorAiCompletionProduct(
                    None,
                    is_valid=False,
                    error=error,
                )

        return InstructorAiCompletionProduct(model_result, is_valid=True)

    def generate_image(self, prompt: str) -> str:
        raise NotImplemented(
            "This LLM client is not meant to be used to generate images."
        )
