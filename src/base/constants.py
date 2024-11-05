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
    "thunderstorm": "fas fa-bolt",
    "drizzle": "fas fa-cloud-rain",
    "sleet": "fas fa-cloud-rain",
    "blazing": "fas fa-temperature-high",
    "heatwave": "fas fa-thermometer-full",
    "dust_storm": "fas fa-smog",
    "sandstorm": "fas fa-smog",
    "tornado": "fas fa-wind",
    "hurricane": "fas fa-wind",
    "blizzard": "fas fa-snowflake",
    "aurora": "fas fa-magic",
    "eclipse": "fas fa-moon",
    "blood_moon": "fas fa-moon",
    "meteor_shower": "fas fa-meteor",
    "acid_rain": "fas fa-radiation",
    "ashfall": "fas fa-smog",
    "volcanic_eruption": "fas fa-fire",
    "solar_flare": "fas fa-bolt",
    "plasma_storm": "fas fa-bolt",
    "radiation_fog": "fas fa-radiation",
    "frost": "fas fa-snowflake",
    "humid": "fas fa-water",
    "dry": "fas fa-sun",
    "sweltering": "fas fa-temperature-high",
    "cold_snap": "fas fa-temperature-low",
    "drought": "fas fa-sun",
    "flood": "fas fa-water",
    "rainbow": "fas fa-star",
    "smog": "fas fa-smog",
    "smoke": "fas fa-smog",
    "glowing_clouds": "fas fa-cloud",
    "ethereal_lights": "fas fa-magic",
    "time_distortion": "fas fa-history",
    "dimensional_rift": "fas fa-exclamation-triangle",
    "blood_rain": "fas fa-tint",
    "magnetic_storm": "fas fa-magnet",
    "psychic_fog": "fas fa-brain",
    "crystal_rain": "fas fa-gem",
    "shadow_eclipse": "fas fa-moon",
    "ghostly_mist": "fas fa-smog",
}
