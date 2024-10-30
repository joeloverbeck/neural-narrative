from typing import Dict

from src.base.enums import TemplateType

DEFAULT_PLAYER_IDENTIFIER = "-1"
DEFAULT_CURRENT_PLACE = "-1"
DEFAULT_IDENTIFIER = "0"

OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1"

REQUEST_OK: int = 200
TOO_MANY_REQUESTS_ERROR_NUMBER: int = 429
UNAUTHORIZED_ERROR_NUMBER: int = 401
PAYMENT_REQUIRED: int = 402
INVALID_SSL_CERTIFICATE: int = 526
MAXIMUM_CONTENT_LENGTH_REACHED: int = 400

PARENT_TEMPLATE_TYPE = {
    TemplateType.WORLD: TemplateType.STORY_UNIVERSE,
    TemplateType.REGION: TemplateType.WORLD,
    TemplateType.AREA: TemplateType.REGION,
    TemplateType.LOCATION: TemplateType.AREA,
}
PARENT_KEYS: Dict[TemplateType, str] = {
    TemplateType.REGION: "world",
    TemplateType.AREA: "region",
    TemplateType.LOCATION: "area",
}
