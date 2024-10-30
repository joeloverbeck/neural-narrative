import logging
from typing import Optional

from openai.types.chat import ChatCompletion

from src.base.constants import (
    TOO_MANY_REQUESTS_ERROR_NUMBER,
    UNAUTHORIZED_ERROR_NUMBER,
    PAYMENT_REQUIRED,
    INVALID_SSL_CERTIFICATE,
    MAXIMUM_CONTENT_LENGTH_REACHED,
)
from src.base.enums import AiCompletionErrorType
from src.prompting.abstracts.ai_completion_product import AiCompletionProduct

logger = logging.getLogger(__name__)


class ConcreteAiCompletionProduct(AiCompletionProduct):

    def __init__(self, completion: Optional[ChatCompletion]):
        self._content = None
        self._error = None
        self._error_details = ""
        if not completion:
            self._is_valid = False
            self._error = AiCompletionErrorType.MALFORMED_COMPLETION
        elif (
            completion.choices
            and completion.choices[0]
            and completion.choices[0].message
            and completion.choices[0].message.content
        ):
            self._is_valid = True
            self._content = completion.choices[0].message.content
        elif (
            hasattr(completion, "error")
            and completion.error["code"] == TOO_MANY_REQUESTS_ERROR_NUMBER
        ):
            self._is_valid = False
            self._error = AiCompletionErrorType.TOO_MANY_REQUESTS
        elif (
            hasattr(completion, "error")
            and completion.error["code"] == UNAUTHORIZED_ERROR_NUMBER
        ):
            self._is_valid = False
            self._error = AiCompletionErrorType.UNAUTHORIZED
        elif (
            hasattr(completion, "error")
            and completion.error["code"] == PAYMENT_REQUIRED
        ):
            self._is_valid = False
            self._error = AiCompletionErrorType.PAYMENT_REQUIRED
            self._error_details = completion.error["message"]
        elif (
            hasattr(completion, "error")
            and completion.error["code"] == INVALID_SSL_CERTIFICATE
        ):
            self._is_valid = False
            self._error = AiCompletionErrorType.INVALID_SSL_CERTIFICATE
            self._error_details = completion.error["message"]
        elif (
            hasattr(completion, "error")
            and completion.error["code"] == MAXIMUM_CONTENT_LENGTH_REACHED
        ):
            self._is_valid = False
            self._error = AiCompletionErrorType.MAXIMUM_CONTENT_LENGTH_REACHED
            self._error_details = completion.error["message"]
        elif not completion.choices:
            self._is_valid = False
            self._error = AiCompletionErrorType.MALFORMED_COMPLETION
        elif not completion.choices[0].message.content:
            self._is_valid = False
            self._error = AiCompletionErrorType.EMPTY_CONTENT
        else:
            self._is_valid = False
            self._error = AiCompletionErrorType.UNHANDLED
            logger.error("Failed due to an unhandled error: %s", self._content)

    def get(self) -> str:
        return self._content

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> AiCompletionErrorType:
        return self._error

    def get_error_details(self) -> str:
        return self._error_details
