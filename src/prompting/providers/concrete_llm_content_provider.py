import logging
from time import sleep

from src.constants import (
    WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR,
    WAIT_TIME_WHEN_UNAUTHORIZED_ERROR,
    WAIT_TIME_WHEN_EMPTY_CONTENT,
    MAX_RETRIES,
    WAIT_TIME_WHEN_MALFORMED_COMPLETION,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.enums import AiCompletionErrorType
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import LlmContentProvider
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.products.concrete_llm_content_product import (
    ConcreteLlmContentProduct,
)

logger = logging.getLogger(__name__)


class ConcreteLlmContentProvider(LlmContentProvider):
    def __init__(
        self,
        model: str,
        messages_to_llm: MessagesToLlm,
        llm_client: LlmClient,
        max_retries=MAX_RETRIES,
        temperature=1.0,
        top_p=1.0,
        filesystem_manager: FilesystemManager = None,
    ):
        if not messages_to_llm:
            raise ValueError("messages_to_llm must not be empty.")
        assert llm_client

        self._model = model
        self._messages_to_llm = messages_to_llm
        self._llm_client = llm_client
        self._max_retries = max_retries
        self._temperature = temperature
        self._top_p = top_p
        self._retry_count = 0

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def generate_content(self) -> LlmContentProduct:
        while self._retry_count < self._max_retries:
            ai_completion_product = self._llm_client.generate_completion(
                model=self._model,
                messages_to_llm=self._messages_to_llm,
                temperature=self._temperature,
                top_p=self._top_p,
            )

            if ai_completion_product.is_valid():
                self._retry_count = 0  # Reset retry count if we get a valid response
                return ConcreteLlmContentProduct(
                    ai_completion_product.get(), is_valid=True
                )

            self._retry_count += 1

            if self._retry_count < self._max_retries:
                if (
                    ai_completion_product.get_error()
                    == AiCompletionErrorType.TOO_MANY_REQUESTS
                ):
                    logger.warning(
                        f"Attempt {self._retry_count}/{self._max_retries} failed due to too many requests. Retrying in {WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR}..."
                    )
                    sleep(WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR)
                elif (
                    ai_completion_product.get_error()
                    == AiCompletionErrorType.UNAUTHORIZED
                ):
                    logger.warning(
                        f"Attempt {self._retry_count}/{self._max_retries} failed due to unauthorized access. Retrying in {WAIT_TIME_WHEN_UNAUTHORIZED_ERROR}..."
                    )
                    sleep(WAIT_TIME_WHEN_UNAUTHORIZED_ERROR)
                elif (
                    ai_completion_product.get_error()
                    == AiCompletionErrorType.MALFORMED_COMPLETION
                ):
                    logger.warning(f"The completion returned by the AI was malformed.")
                    sleep(WAIT_TIME_WHEN_MALFORMED_COMPLETION)
                elif (
                    ai_completion_product.get_error()
                    == AiCompletionErrorType.EMPTY_CONTENT
                ):
                    logger.warning(
                        f"Attempt {self._retry_count}/{self._max_retries} failed due to empty content returned by LLM. Retrying in {WAIT_TIME_WHEN_EMPTY_CONTENT}..."
                    )

                    empty_content_context_file_path = (
                        self._filesystem_manager.get_file_path_to_empty_content_context_file()
                    )

                    self._filesystem_manager.create_empty_file_if_not_exists(
                        empty_content_context_file_path
                    )

                    # Store the messages for testing purposes.
                    self._filesystem_manager.save_json_file(
                        self._messages_to_llm.get(),
                        empty_content_context_file_path,
                    )

                    raise ValueError(
                        "The LLM returned empty content. That may mean that the context is too long."
                    )
                elif (
                    ai_completion_product.get_error()
                    == AiCompletionErrorType.PAYMENT_REQUIRED
                ):
                    raise ValueError(
                        f"The LLM won't produce content because you've run out of credits. Details: {ai_completion_product.get_error_details()}"
                    )
                else:
                    logger.warning(
                        f"Attempt {self._retry_count}/{self._max_retries} failed due to an unhandled reason. Retrying..."
                    )

        return ConcreteLlmContentProduct(
            content="", is_valid=False, error="Max retries reached. No valid response."
        )
