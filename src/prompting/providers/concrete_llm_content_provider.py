import logging
from typing import Optional, Type

from pydantic import BaseModel

from src.base.enums import AiCompletionErrorType
from src.dialogues.messages_to_llm import MessagesToLlm
from src.filesystem.file_operations import (
    create_empty_file_if_not_exists,
    write_json_file,
    create_directories,
)
from src.filesystem.path_manager import PathManager
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
        path_manager: Optional[PathManager] = None,
    ):
        self._llm = llm
        self._messages_to_llm = messages_to_llm
        self._llm_client_factory = llm_client_factory

        self._path_manager = path_manager or PathManager()

    def generate_content(self, response_model: Type[BaseModel]) -> LlmContentProduct:
        ai_completion_product = self._llm_client_factory.create_llm_client(
            self._llm, response_model
        ).generate_completion(
            model=self._llm,
            messages_to_llm=self._messages_to_llm,
        )

        if ai_completion_product.is_valid():
            content = ai_completion_product.get()

            if isinstance(content, BaseModel):
                return BaseModelLlmContentProduct(content, is_valid=True)
            else:
                raise NotImplemented(
                    f"Case not handled for content being of type '{type(content)}'"
                )

        error = ai_completion_product.get_error()

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

            # Ensure the errors folder exists to begin with
            create_directories(self._path_manager.get_errors_path())

            empty_content_context_file_path = (
                self._path_manager.get_empty_content_context_path()
            )
            create_empty_file_if_not_exists(empty_content_context_file_path)

            write_json_file(
                empty_content_context_file_path, self._messages_to_llm.get()
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
            error=f"Max retries reached. No valid response. Error: {error}",
        )
