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

PARENT_TEMPLATE_TYPE: Dict[TemplateType, TemplateType] = {
    TemplateType.WORLD: TemplateType.STORY_UNIVERSE,
    TemplateType.REGION: TemplateType.WORLD,
    TemplateType.AREA: TemplateType.REGION,
    TemplateType.LOCATION: TemplateType.AREA,
    TemplateType.ROOM: TemplateType.LOCATION,
}

CHILD_TEMPLATE_TYPE: Dict[TemplateType, TemplateType] = {
    TemplateType.STORY_UNIVERSE: TemplateType.WORLD,
    TemplateType.WORLD: TemplateType.REGION,
    TemplateType.REGION: TemplateType.AREA,
    TemplateType.AREA: TemplateType.LOCATION,
    TemplateType.LOCATION: TemplateType.ROOM,
}

PARENT_KEYS: Dict[TemplateType, str] = {
    TemplateType.REGION: "world",
    TemplateType.AREA: "region",
    TemplateType.LOCATION: "area",
    TemplateType.ROOM: "location",
}

CHILDREN_KEYS: Dict[TemplateType, str] = {
    TemplateType.AREA: "locations",
    TemplateType.LOCATION: "rooms",
}

WEATHER_ICON_MAPPING = {
    "sunny": "fas fa-sun",
    "rainy": "fas fa-cloud-showers-heavy",
    "cloudy": "fas fa-cloud",
    "stormy": "fas fa-cloud-bolt",
    "snowy": "fas fa-snowflake",
    "foggy": "fas fa-smog",
    "windy": "fas fa-wind",
    "misty": "fas fa-smog",
    "hail": "fas fa-cloud-rain",
    "overcast": "fas fa-cloud",
}
