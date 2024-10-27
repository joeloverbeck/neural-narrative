from pathlib import Path
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

CHARACTER_INFORMATION_BLOCK: str = "data/prompting/blocks/character_information.txt"
PLACES_DESCRIPTIONS_BLOCK: str = "data/prompting/blocks/places_descriptions.txt"
PLAYER_AND_FOLLOWERS_INFORMATION_BLOCK: str = (
    "data/prompting/blocks/player_and_followers_information.txt"
)
CHARACTER_GENERATION_INSTRUCTIONS_FILE: str = (
    "data/prompting/characters/base_character_data_generation_prompt.txt"
)
SPEECH_PATTERNS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/speech_patterns_generation_prompt.txt"
)
TOOL_INSTRUCTIONS_FOR_INSTRUCTOR_FILE: str = (
    "data/prompting/tool_instructions_for_instructor.txt"
)
DIALOGUE_PROMPT_FILE: str = "data/prompting/dialogues/dialogue_prompt.txt"
CHOOSING_SPEECH_TURN_PROMPT_FILE: str = (
    "data/prompting/dialogues/choosing_speech_turn_prompt.txt"
)
SUMMARIZE_DIALOGUE_PROMPT_FILE: str = (
    "data/prompting/dialogues/summarize_dialogue_prompt.txt"
)
STORY_UNIVERSE_GENERATION_PROMPT_FILE: str = (
    "data/prompting/base/story_universe_generation_prompt.txt"
)
WORLD_GENERATION_PROMPT_FILE: Path = Path(
    "data/prompting/places/world_generation_prompt.txt"
)
REGION_GENERATION_PROMPT_FILE: Path = Path(
    "data/prompting/places/region_generation_prompt.txt"
)
AREA_GENERATION_PROMPT_FILE: Path = Path(
    "data/prompting/places/area_generation_prompt.txt"
)
LOCATION_GENERATION_PROMPT_FILE: Path = Path(
    "data/prompting/places/location_generation_prompt.txt"
)
PLACE_DESCRIPTION_PROMPT_FILE: str = (
    "data/prompting/places/place_description_prompt.txt"
)
TRAVEL_NARRATION_PROMPT_FILE: str = "data/prompting/places/travel_narration_prompt.txt"
CHARACTER_GENERATION_GUIDELINES_PROMPT_FILE: str = (
    "data/prompting/characters/character_generation_guidelines_prompt.txt"
)
SCENARIOS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/scenarios_generation_prompt.txt"
)
DILEMMAS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/dilemmas_generation_prompt.txt"
)
IMAGE_GENERATION_PROMPT_FILE: str = "data/prompting/image_generation_prompt.txt"
CHARACTER_DESCRIPTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/character_description_generation_prompt.txt"
)
PLOT_BLUEPRINTS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/plot_blueprints_generation_prompt.txt"
)
AMBIENT_NARRATION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/dialogues/ambient_narration_generation_prompt.txt"
)
SELF_REFLECTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/self_reflection_generation_prompt.txt"
)
GOALS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/goals_generation_prompt.txt"
)
PLOT_TWISTS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/plot_twists_generation_prompt.txt"
)
RESEARCH_RESOLUTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/actions/research_resolution_generation_prompt.txt"
)
INVESTIGATE_RESOLUTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/actions/investigate_resolution_generation_prompt.txt"
)
GATHER_SUPPLIES_RESOLUTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/actions/gather_supplies_resolution_generation_prompt.txt"
)
SECRETS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/secrets_generation_prompt.txt"
)
CONNECTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/connection_generation_prompt.txt"
)
