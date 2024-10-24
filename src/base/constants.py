from typing import Dict

from src.base.enums import TemplateType

DEFAULT_PLAYER_IDENTIFIER = "-1"
DEFAULT_CURRENT_PLACE = "-1"
DEFAULT_IDENTIFIER = "0"
DEFAULT_VOICE_MODEL = "malewarlock"
NARRATOR_VOICE_MODEL = "tulius"
MAX_DIALOGUE_ENTRIES_FOR_WEB = 10
TIME_ADVANCED_DUE_TO_DIALOGUE = 1
TIME_ADVANCED_DUE_TO_EXITING_LOCATION = 1
TIME_ADVANCED_DUE_TO_TRAVELING = 10
TIME_ADVANCED_DUE_TO_SEARCHING_FOR_LOCATION = 2
MAX_RETRIES: int = 10
MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE: int = 3
MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL: int = 3
REQUEST_OK: int = 200
TOO_MANY_REQUESTS_ERROR_NUMBER: int = 429
UNAUTHORIZED_ERROR_NUMBER: int = 401
PAYMENT_REQUIRED: int = 402
INVALID_SSL_CERTIFICATE: int = 526
WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR: int = 10
WAIT_TIME_WHEN_UNAUTHORIZED_ERROR: int = 10
WAIT_TIME_WHEN_EMPTY_CONTENT: int = 5
WAIT_TIME_WHEN_MALFORMED_COMPLETION: int = 5
CONFIG_FILE: str = "data/llm/config.json"
XTTS_CONFIG_FILE: str = "data/voices/xtts_config.json"
LOGGING_CONFIG_FILE: str = "data/logging/logging_config.json"
VOICE_MODELS_FILE: str = "data/voices/voice_models.json"
VOICE_LINES_FOLDER_PATH: str = "static/voice_lines"
PLAYTHROUGHS_FOLDER: str = "playthroughs"
CHARACTERS_FOLDER_NAME: str = "characters"
IMAGES_FOLDER_NAME: str = "images"
ONGOING_DIALOGUE_FOLDER_NAME: str = "ongoing dialogue"
ONGOING_DIALOGUE_FILE: str = "ongoing_dialogue.json"
DEFAULT_IMAGE_FILE: str = "static/images/default.png"
PLAYTHROUGH_METADATA_FILE: str = "playthrough_metadata.json"
MAP_FILE: str = "map.json"
CHARACTERS_FILE: str = "characters.json"
MEMORIES_FILE: str = "memories.txt"
DIALOGUES_FILE: str = "dialogues.txt"
CHARACTER_GENERATION_GUIDELINES_FILE: str = (
    "data/guidelines/character_generation_guidelines.json"
)
OPENROUTER_SECRET_KEY_FILE: str = "OPENROUTER_SECRET_KEY.txt"
OPENAI_SECRET_KEY_FILE: str = "OPENAI_SECRET_KEY.txt"
OPENAI_PROJECT_KEY_FILE: str = "OPENAI_PROJECT_KEY.txt"
RUNPOD_SECRET_KEY_FILE: str = "RUNPOD_SECRET_KEY.txt"
WEATHERS_FILE: str = "data/weathers/weathers.json"
STORY_UNIVERSES_TEMPLATE_FILE: str = "data/templates/story_universes.json"
WORLDS_TEMPLATES_FILE: str = "data/templates/worlds.json"
REGIONS_TEMPLATES_FILE: str = "data/templates/regions.json"
AREAS_TEMPLATES_FILE: str = "data/templates/areas.json"
LOCATIONS_TEMPLATES_FILE: str = "data/templates/locations.json"
PARENT_TEMPLATE_TYPE = {
    TemplateType.WORLD: TemplateType.STORY_UNIVERSE,
    TemplateType.REGION: TemplateType.WORLD,
    TemplateType.AREA: TemplateType.REGION,
    TemplateType.LOCATION: TemplateType.AREA,
}
TEMPLATE_FILES = {
    TemplateType.STORY_UNIVERSE: STORY_UNIVERSES_TEMPLATE_FILE,
    TemplateType.WORLD: WORLDS_TEMPLATES_FILE,
    TemplateType.REGION: REGIONS_TEMPLATES_FILE,
    TemplateType.AREA: AREAS_TEMPLATES_FILE,
    TemplateType.LOCATION: LOCATIONS_TEMPLATES_FILE,
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
SPEECH_PATTERNS_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/speech_patterns_generation_tool.json"
)
SPEECH_GENERATOR_TOOL_FILE: str = "data/prompting/speech_generator_tool.json"
SPEECH_TURN_TOOL_FILE: str = "data/prompting/speech_turn_tool.json"
DIALOGUE_SUMMARIZATION_TOOL_FILE: str = (
    "data/prompting/dialogue_summarization_tool.json"
)
STORY_UNIVERSE_GENERATION_TOOL_FILE: str = (
    "data/prompting/base/story_universe_generation_tool.json"
)
WORLD_GENERATION_TOOL_FILE: str = "data/prompting/places/world_generation_tool.json"
REGION_GENERATION_TOOL_FILE: str = "data/prompting/places/region_generation_tool.json"
AREA_GENERATION_TOOL_FILE: str = "data/prompting/places/area_generation_tool.json"
LOCATION_GENERATION_TOOL_FILE: str = (
    "data/prompting/places/location_generation_tool.json"
)
PLACE_DESCRIPTION_TOOL_FILE: str = "data/prompting/places/place_description_tool.json"
TRAVEL_NARRATION_TOOL_FILE: str = "data/prompting/places/travel_narration_tool.json"
CHARACTER_DESCRIPTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/character_description_generation_tool.json"
)
AMBIENT_NARRATION_GENERATION_TOOL_FILE: str = (
    "data/prompting/ambient_narration_generation_tool.json"
)
SELF_REFLECTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/self_reflection_generation_tool.json"
)
GOAL_RESOLUTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/goal_resolution_generation_tool.json"
)
RESEARCH_RESOLUTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/actions/research_resolution_generation_tool.json"
)
INVESTIGATE_RESOLUTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/actions/investigate_resolution_generation_tool.json"
)
GATHER_SUPPLIES_RESOLUTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/actions/gather_supplies_resolution_generation_tool.json"
)
SECRETS_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/secrets_generation_tool.json"
)
CONNECTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/connection_generation_tool.json"
)
CHARACTER_GENERATION_INSTRUCTIONS_FILE: str = (
    "data/prompting/characters/base_character_data_generation_prompt.txt"
)
SPEECH_PATTERNS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/speech_patterns_generation_prompt.txt"
)
TOOL_INSTRUCTIONS_FILE: str = "data/prompting/tool_instructions.txt"
TOOL_INSTRUCTIONS_FOR_INSTRUCTOR_FILE: str = (
    "data/prompting/tool_instructions_for_instructor.txt"
)
DIALOGUE_PROMPT_FILE: str = "data/prompting/dialogue_prompt.txt"
CHOOSING_SPEECH_TURN_PROMPT_FILE: str = "data/prompting/choosing_speech_turn_prompt.txt"
SUMMARIZE_DIALOGUE_PROMPT_FILE: str = "data/prompting/summarize_dialogue_prompt.txt"
STORY_UNIVERSE_GENERATION_PROMPT_FILE: str = (
    "data/prompting/base/story_universe_generation_prompt.txt"
)
WORLD_GENERATION_PROMPT_FILE: str = "data/prompting/places/world_generation_prompt.txt"
REGION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/places/region_generation_prompt.txt"
)
AREA_GENERATION_PROMPT_FILE: str = "data/prompting/places/area_generation_prompt.txt"
LOCATION_GENERATION_PROMPT_FILE: str = (
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
INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE: str = (
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
    "data/prompting/ambient_narration_generation_prompt.txt"
)
SELF_REFLECTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/self_reflection_generation_prompt.txt"
)
GOAL_RESOLUTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/goal_resolution_generation_prompt.txt"
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
OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1"

LLMS_FILE: str = "data/llm/llms.json"

LOCATION_TYPES = [
    "APARTMENT_BUILDING",
    "BAR",
    "BURIAL_SITE",
    "BROTHEL",
    "CAVE_SYSTEM",
    "CHAMBER",
    "CLEARING",
    "COLLEGE",
    "FORGE",
    "FORTRESS",
    "GREENHOUSE",
    "HOSPITAL",
    "INN",
    "LABYRINTH",
    "LIBRARY",
    "MALL",
    "MANSION",
    "MINE",
    "OASIS",
    "PARK",
    "POLICE_STATION",
    "TRAINING_GROUND",
    "WOODS",
    "OTHER",
]
