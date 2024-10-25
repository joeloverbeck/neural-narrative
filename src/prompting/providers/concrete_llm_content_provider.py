import logging
from typing import Optional, Type

from pydantic import BaseModel

from src.base.enums import AiCompletionErrorType
from src.dialogues.messages_to_llm import MessagesToLlm
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.abstract_factories import (
    LlmContentProvider,
    LlmClientFactory,
)
from src.prompting.abstracts.factory_products import LlmContentProduct
from src.prompting.llm import Llm
from src.prompting.products.base_model_llm_content_product import (
    BaseModelLlmContentProduct,
)
from src.prompting.products.unparsed_llm_content_product import (
    UnparsedLlmContentProduct,
)

logger = logging.getLogger(__name__)


class ConcreteLlmContentProvider(LlmContentProvider):

    def __init__(
        self,
        llm: Llm,
        messages_to_llm: MessagesToLlm,
        llm_client_factory: LlmClientFactory,
        temperature=1.0,
        top_p=1.0,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._llm = llm
        self._messages_to_llm = messages_to_llm
        self._llm_client_factory = llm_client_factory
        self._temperature = temperature
        self._top_p = top_p
        self._retry_count = 0

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def generate_content(self, response_model: Type[BaseModel]) -> LlmContentProduct:
        ai_completion_product = self._llm_client_factory.create_llm_client(
            self._llm, response_model
        ).generate_completion(
            model=self._llm.get_name(),
            messages_to_llm=self._messages_to_llm,
            temperature=self._temperature,
            top_p=self._top_p,
        )

        if ai_completion_product.is_valid():
            self._retry_count = 0
            content = ai_completion_product.get()

            if isinstance(content, str):
                return UnparsedLlmContentProduct(content, is_valid=True)
            elif isinstance(content, BaseModel):
                return BaseModelLlmContentProduct(content, is_valid=True)
            else:
                raise NotImplemented(
                    f"Case not handled for content being of type '{type(content)}'"
                )

        if ai_completion_product.get_error() == AiCompletionErrorType.TOO_MANY_REQUESTS:
            logger.warning(f"Attempt failed due to too many requests.")
        elif ai_completion_product.get_error() == AiCompletionErrorType.UNAUTHORIZED:
            logger.warning(f"Attempt failed due to unauthorized access.")
        elif (
            ai_completion_product.get_error()
            == AiCompletionErrorType.MALFORMED_COMPLETION
        ):
            logger.warning(f"The completion returned by the AI was malformed.")
        elif ai_completion_product.get_error() == AiCompletionErrorType.EMPTY_CONTENT:
            logger.warning(f"Attempt failed due to empty content returned by LLM.")
            empty_content_context_file_path = (
                self._filesystem_manager.get_file_path_to_empty_content_context_file()
            )
            self._filesystem_manager.create_empty_file_if_not_exists(
                empty_content_context_file_path
            )
            self._filesystem_manager.save_json_file(
                self._messages_to_llm.get(), empty_content_context_file_path
            )
            logger.warning(
                "The LLM returned empty content. That may mean that the context is too long."
            )
        elif (
            ai_completion_product.get_error() == AiCompletionErrorType.PAYMENT_REQUIRED
        ):
            raise ValueError(
                f"The LLM won't produce content because you've run out of credits. Details: {ai_completion_product.get_error_details()}"
            )
        elif (
            ai_completion_product.get_error()
            == AiCompletionErrorType.INVALID_SSL_CERTIFICATE
        ):
            raise ValueError(
                f"The LLM indicated that the SSL certificate was invalid. Details: {ai_completion_product.get_error_details()}"
            )
        else:
            logger.warning(f"Attempt failed due to an unhandled reason.")

        return UnparsedLlmContentProduct(
            content="",
            is_valid=False,
            error="Max retries reached. No valid response.",
        )
