from enum import Enum


# Enum definition for identifier types
class IdentifierType(Enum):
    PLACES = "places"
    CHARACTERS = "characters"


class AiCompletionErrorType(Enum):
    TOO_MANY_REQUESTS = "too_many_requests"
    UNAUTHORIZED = "unauthorized"
    EMPTY_CONTENT = "empty_content"
    MALFORMED_COMPLETION = "malformed_completion"
    UNHANDLED = "unhandled"
