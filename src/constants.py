MAX_RETRIES: int = 10
MAX_RETRIES_WHEN_UNRECOVERABLE_SPEECH_TURN_CHOICE: int = 3
MAX_RETRIES_WHEN_FAILED_TO_RETURN_FUNCTION_CALL: int = 3
TOO_MANY_REQUESTS_ERROR_NUMBER: int = 429
UNAUTHORIZED_ERROR_NUMBER: int = 401
WAIT_TIME_WHEN_TOO_MANY_REQUESTS_ERROR: int = 10
WAIT_TIME_WHEN_UNAUTHORIZED_ERROR: int = 10
WAIT_TIME_WHEN_EMPTY_CONTENT: int = 5
WAIT_TIME_WHEN_MALFORMED_COMPLETION: int = 5

PLAYTHROUGHS_FOLDER: str = "playthroughs"
CHARACTERS_FOLDER_NAME: str = "characters"
PLAYTHROUGH_METADATA_FILE: str = "playthrough_metadata.json"
MAP_FILE: str = "map.json"
CHARACTERS_FILE: str = "characters.json"
MEMORIES_FILE: str = "memories.txt"
DIALOGUES_FILE: str = "dialogues.txt"
SECRET_KEY_FILE: str = "GPT_SECRET_KEY.txt"
WORLD_TEMPLATES_FILE: str = "data/templates/worlds.json"
LOCATIONS_TEMPLATES_FILE: str = "data/templates/locations.json"
AREAS_TEMPLATES_FILE: str = "data/templates/areas.json"
CHARACTER_GENERATOR_TOOL_FILE: str = "data/prompting/character_generator_tool.json"
SPEECH_GENERATOR_TOOL_FILE: str = "data/prompting/speech_generator_tool.json"
SPEECH_TURN_TOOL_FILE: str = "data/prompting/speech_turn_tool.json"
DIALOGUE_SUMMARIZATION_TOOL_FILE: str = "data/prompting/dialogue_summarization_tool.json"
CHARACTER_GENERATION_INSTRUCTIONS_FILE: str = "data/prompting/character_generation_instructions.txt"
TOOL_INSTRUCTIONS_FILE: str = "data/prompting/tool_instructions.txt"
DIALOGUE_PROMPT_FILE: str = "data/prompting/dialogue_prompt.txt"
CHOOSING_SPEECH_TURN_PROMPT_FILE: str = "data/prompting/choosing_speech_turn_prompt.txt"
SUMMARIZE_DIALOGUE_PROMPT_FILE: str = "data/prompting/summarize_dialogue_prompt.txt"

OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1"
HERMES_405B = "nousresearch/hermes-3-llama-3.1-405b"
HERMES_70B = "nousresearch/hermes-3-llama-3.1-70b"
