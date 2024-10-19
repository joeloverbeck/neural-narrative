from enum import Enum


# Enum definition for identifier types
class IdentifierType(Enum):
    PLACES = "places"
    CHARACTERS = "characters"


class PlaceType(Enum):
    LOCATION = "location"
    AREA = "area"
    REGION = "region"
    WORLD = "world"


class TemplateType(Enum):
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
    UNHANDLED = "unhandled"
