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
WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR: int = 10
WAIT_TIME_WHEN_UNAUTHORIZED_ERROR: int = 10
WAIT_TIME_WHEN_EMPTY_CONTENT: int = 5
WAIT_TIME_WHEN_MALFORMED_COMPLETION: int = 5

# Base files and folders

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

# Templates

WORLD_TEMPLATES_FILE: str = "data/templates/worlds.json"
REGIONS_TEMPLATES_FILE: str = "data/templates/regions.json"
AREAS_TEMPLATES_FILE: str = "data/templates/areas.json"
LOCATIONS_TEMPLATES_FILE: str = "data/templates/locations.json"

# Prompting Blocks
CHARACTER_INFORMATION_BLOCK: str = "data/prompting/blocks/character_information.txt"
PLACES_DESCRIPTIONS_BLOCK: str = "data/prompting/blocks/places_descriptions.txt"
PLAYER_AND_FOLLOWERS_INFORMATION_BLOCK: str = (
    "data/prompting/blocks/player_and_followers_information.txt"
)

# Tools

CHARACTER_GENERATOR_TOOL_FILE: str = (
    "data/prompting/characters/character_generation_tool.json"
)
SPEECH_GENERATOR_TOOL_FILE: str = "data/prompting/speech_generator_tool.json"
SPEECH_TURN_TOOL_FILE: str = "data/prompting/speech_turn_tool.json"
DIALOGUE_SUMMARIZATION_TOOL_FILE: str = (
    "data/prompting/dialogue_summarization_tool.json"
)
WORLD_GENERATION_TOOL_FILE: str = "data/prompting/places/world_generation_tool.json"
REGION_GENERATION_TOOL_FILE: str = "data/prompting/places/region_generation_tool.json"
AREA_GENERATION_TOOL_FILE: str = "data/prompting/places/area_generation_tool.json"
LOCATION_GENERATION_TOOL_FILE: str = (
    "data/prompting/places/location_generation_tool.json"
)
PLACE_DESCRIPTION_TOOL_FILE: str = "data/prompting/places/place_description_tool.json"
TRAVEL_NARRATION_TOOL_FILE: str = "data/prompting/places/travel_narration_tool.json"
CHARACTER_GENERATION_GUIDELINES_TOOL_FILE: str = (
    "data/prompting/characters/character_generation_guidelines_tool.json"
)
INTERESTING_SITUATIONS_GENERATION_TOOL_FILE: str = (
    "data/prompting/concepts/interesting_situations_generation_tool.json"
)
INTERESTING_DILEMMAS_GENERATION_TOOL_FILE: str = (
    "data/prompting/concepts/interesting_dilemmas_generation_tool.json"
)
CHARACTER_DESCRIPTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/character_description_generation_tool.json"
)
CONCEPTS_GENERATION_TOOL_FILE: str = (
    "data/prompting/concepts/concepts_generation_tool.json"
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
GOALS_GENERATION_TOOL_FILE: str = "data/prompting/concepts/goals_generation_tool.json"
RESEARCH_RESOLUTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/actions/research_resolution_generation_tool.json"
)
INVESTIGATE_RESOLUTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/actions/investigate_resolution_generation_tool.json"
)
SECRETS_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/secrets_generation_tool.json"
)
CONNECTION_GENERATION_TOOL_FILE: str = (
    "data/prompting/characters/connection_generation_tool.json"
)

# Prompts

CHARACTER_GENERATION_INSTRUCTIONS_FILE: str = (
    "data/prompting/characters/character_generation_prompt.txt"
)
TOOL_INSTRUCTIONS_FILE: str = "data/prompting/tool_instructions.txt"
DIALOGUE_PROMPT_FILE: str = "data/prompting/dialogue_prompt.txt"
CHOOSING_SPEECH_TURN_PROMPT_FILE: str = "data/prompting/choosing_speech_turn_prompt.txt"
SUMMARIZE_DIALOGUE_PROMPT_FILE: str = "data/prompting/summarize_dialogue_prompt.txt"
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
INTERESTING_SITUATIONS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/interesting_situations_generation_prompt.txt"
)
INTERESTING_DILEMMAS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/interesting_dilemmas_generation_prompt.txt"
)
IMAGE_GENERATION_PROMPT_FILE: str = "data/prompting/image_generation_prompt.txt"
CHARACTER_DESCRIPTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/character_description_generation_prompt.txt"
)
CONCEPTS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/concepts/concepts_generation_prompt.txt"
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
RESEARCH_RESOLUTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/actions/research_resolution_generation_prompt.txt"
)
INVESTIGATE_RESOLUTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/actions/investigate_resolution_generation_prompt.txt"
)
SECRETS_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/secrets_generation_prompt.txt"
)
CONNECTION_GENERATION_PROMPT_FILE: str = (
    "data/prompting/characters/connection_generation_prompt.txt"
)

OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1"

# LLMs

HERMES_405B = "nousresearch/hermes-3-llama-3.1-405b"
HERMES_405B_FREE = "nousresearch/hermes-3-llama-3.1-405b:free"
HERMES_70B = "nousresearch/hermes-3-llama-3.1-70b"

# Voice attributes

VOICE_GENDERS = ["MALE", "FEMALE"]

VOICE_AGES = ["CHILDLIKE", "TEENAGE", "YOUNG ADULT/ADULT", "MIDDLE-AGED", "ELDERLY"]

VOICE_EMOTIONS = [
    "CALM",
    "HAPPY/JOYFUL",
    "SAD/MELANCHOLIC",
    "ANGRY/AGGRESSIVE",
    "ANXIOUS/FRIGHTENED",
    "CONFIDENT/DETERMINED",
    "HOPEFUL",
    "SURPRISED",
    "PLAYFUL",
    "EXCITED",
]

VOICE_TEMPOS = ["FAST", "SLOW", "MODERATE"]

VOICE_VOLUMES = [
    "WHISPERING",
    "SOFT-SPOKEN/QUIET",
    "NORMAL VOLUME",
    "LOUD",
]

VOICE_TEXTURES = [
    "GRAVELLY/RASPY",
    "SMOOTH",
    "NASAL",
    "CRISP",
    "MUFFLED",
    "WHISPERY/AIRY",
    "METALLIC/MECHANICAL",
    "GUTTURAL",
]

VOICE_TONES = ["WARM", "NEUTRAL", "COLD", "AUTHORITATIVE"]

VOICE_STYLES = [
    "FORMAL",
    "CASUAL",
    "INTENSE/DRAMATIC",
    "MONOTONE",
    "DRAWLING",
    "FLIRTATIOUS",
    "HUMOROUS/SARCASTIC",
    "MELODIC",
    "NARRATIVE",
    "INSTRUCTIONAL",
]

VOICE_PERSONALITIES = [
    "INNOCENT/NAIVE",
    "YOUTHFUL",
    "ENERGETIC",
    "HEROIC/BRAVE",
    "PASSIONATE",
    "ADVENTUROUS/DRIVEN",
    "OPTIMISTIC",
    "NOBLE",
    "SULTRY",
    "WITTY",
    "KIND",
    "CHARMING",
    "WISE/PHILOSOPHICAL",
    "STOIC",
    "ECCENTRIC",
    "MYSTERIOUS",
    "SKEPTICAL",
    "WORLD-WEARY",
    "CYNICAL/PESSIMISTIC",
    "PARANOID",
    "MANIPULATIVE/SCHEMING",
    "SLY",
    "VILLAINOUS",
]

VOICE_SPECIAL_EFFECTS = [
    "NO SPECIAL EFFECTS",
    "ROBOTIC/SYNTHESIZED",
    "ALIEN",
    "DEMON-LIKE",
    "MAGICAL",
    "DISTORTED",
    "GHOSTLY/ECHOED",
    "RETRO",
]

LOCATION_TYPES = [
    "BAR",
    "POLICE STATION",
    "BROTHEL",
    "MALL",
    "APARTMENT BUILDING",
    "MANSION",
    "CAVE SYSTEM",
    "LABYRINTH",
    "BURIAL SITE",
    "FORTRESS",
    "HOSPITAL",
    "TRAINING GROUND",
    "FORGE",
    "CHAMBER",
    "INN",
    "MINE",
    "OASIS",
    "GREENHOUSE",
    "CLEARING",
    "WOODS",
    "COLLEGE",
]
