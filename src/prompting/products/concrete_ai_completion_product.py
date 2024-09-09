from typing import Optional

from openai.types.chat import ChatCompletion

from src.constants import TOO_MANY_REQUESTS_ERROR_NUMBER, UNAUTHORIZED_ERROR_NUMBER
from src.enums import AiCompletionErrorType
from src.prompting.abstracts.factory_products import AiCompletionProduct


class ConcreteAiCompletionProduct(AiCompletionProduct):
    def __init__(self, completion: Optional[ChatCompletion]):
        # upon receiving the completion on creation,
        # the class will establish what the problem is, if any.
        self._content = None
        self._error = None

        if not completion:
            self._is_valid = False
            self._error = AiCompletionErrorType.MALFORMED_COMPLETION
        elif completion.choices and completion.choices[0] and completion.choices[0].message and completion.choices[
            0].message.content:
            self._is_valid = True

            # Store the content
            self._content = completion.choices[0].message.content
        elif hasattr(completion, 'error') and completion.error['code'] == TOO_MANY_REQUESTS_ERROR_NUMBER:
            self._is_valid = False
            self._error = AiCompletionErrorType.TOO_MANY_REQUESTS
        elif hasattr(completion, 'error') and completion.error['code'] == UNAUTHORIZED_ERROR_NUMBER:
            self._is_valid = False
            self._error = AiCompletionErrorType.UNAUTHORIZED
        elif not completion.choices:
            self._is_valid = False
            self._error = AiCompletionErrorType.MALFORMED_COMPLETION
        elif not completion.choices[0].message.content:
            self._is_valid = False
            self._error = AiCompletionErrorType.EMPTY_CONTENT
        else:
            # failed due to unhandled error
            self._is_valid = False
            self._error = AiCompletionErrorType.UNHANDLED
            print(self._content)

    def get(self) -> str:
        return self._content

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> AiCompletionErrorType:
        return self._error
