from enum import Enum


class IdentifierType(Enum):
    PLACES = "places"
    CHARACTERS = "characters"


class TemplateType(Enum):
    ROOM = "room"
    LOCATION = "location"
    AREA = "area"
    REGION = "region"
    WORLD = "world"
    STORY_UNIVERSE = "story_universe"


class AiCompletionErrorType(Enum):
    TOO_MANY_REQUESTS = "too_many_requests"
    UNAUTHORIZED = "unauthorized"
    EMPTY_CONTENT = "empty_content"
    MALFORMED_COMPLETION = "malformed_completion"
    PAYMENT_REQUIRED = "payment_required"
    INVALID_SSL_CERTIFICATE = "invalid_ssl_certificate"
    MAXIMUM_CONTENT_LENGTH_REACHED = "maximum_content_length_reached"
    VALIDATION = "validation"
    UNHANDLED = "unhandled"
