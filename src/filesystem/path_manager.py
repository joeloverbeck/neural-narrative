# src.filesystem.path_manager.py
from datetime import datetime
from pathlib import Path

from src.base.enums import TemplateType
from src.concepts.enums import ConceptType


class PathManager:
    TEMPLATE_FILES = {
        TemplateType.LOCATION: "locations.json",
        TemplateType.AREA: "areas.json",
        TemplateType.REGION: "regions.json",
        TemplateType.WORLD: "worlds.json",
        TemplateType.STORY_UNIVERSE: "story_universes.json",
    }

    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    PLAYTHROUGHS_DIR = BASE_DIR / "playthroughs"
    ERRORS_DIR = BASE_DIR / "errors"

    TEMPLATES_DIR = DATA_DIR / "templates"
    PLACES_DIR = DATA_DIR / "places"
    LOGGING_DIR = DATA_DIR / "logging"
    VOICES_DIR = DATA_DIR / "voices"
    GUIDELINES_DIR = DATA_DIR / "guidelines"
    WEATHERS_DIR = DATA_DIR / "weathers"
    LLMS_DIR = DATA_DIR / "llms"

    PROMPTING_DIR = DATA_DIR / "prompting"
    PROMPTING_IMAGES_DIR = PROMPTING_DIR / "images"
    PROMPTING_BASE_DIR = PROMPTING_DIR / "base"
    ACTIONS_DIR = PROMPTING_DIR / "actions"
    BLOCKS_DIR = PROMPTING_DIR / "blocks"
    PROMPTING_PLACES_DIR = PROMPTING_DIR / "places"
    DIALOGUES_DIR = PROMPTING_DIR / "dialogues"
    PROMPTING_CHARACTERS_DIR = PROMPTING_DIR / "characters"
    CONCEPTS_DIR = PROMPTING_DIR / "concepts"

    STATIC_DIR = BASE_DIR / "static"
    IMAGES_DIR = STATIC_DIR / "images"
    VOICE_LINES_DIR = STATIC_DIR / "voice_lines"
    STATIC_PLAYTHROUGHS_DIR = STATIC_DIR / "playthroughs"

    @classmethod
    def get_openai_project_key_path(cls) -> Path:
        return cls.BASE_DIR / "OPENAI_PROJECT_KEY.txt"

    @classmethod
    def get_openai_secret_key_path(cls) -> Path:
        return cls.BASE_DIR / "OPENAI_SECRET_KEY.txt"

    @classmethod
    def get_openrouter_secret_key_path(cls) -> Path:
        return cls.BASE_DIR / "OPENROUTER_SECRET_KEY.txt"

    @classmethod
    def get_runpod_secret_key_path(cls) -> Path:
        return cls.BASE_DIR / "RUNPOD_SECRET_KEY.txt"

    @classmethod
    def get_config_path(cls) -> Path:
        return cls.BASE_DIR / "config.json"

    @classmethod
    def get_logging_config(cls) -> Path:
        return cls.LOGGING_DIR / "logging_config.json"

    @classmethod
    def get_xtts_config_path(cls) -> Path:
        return cls.VOICES_DIR / "xtts_config.json"

    @classmethod
    def get_voice_models_path(cls) -> Path:
        return cls.VOICES_DIR / "voice_models.json"

    @classmethod
    def get_character_generation_guidelines_path(cls) -> Path:
        return cls.GUIDELINES_DIR / "character_generation_guidelines.json"

    @classmethod
    def get_weathers_path(cls) -> Path:
        return cls.WEATHERS_DIR / "weathers.json"

    @classmethod
    def get_llms_path(cls) -> Path:
        return cls.LLMS_DIR / "llms.json"

    @classmethod
    def get_temp_voice_lines_path(cls, timestamp: str) -> Path:
        return cls.BASE_DIR / "temp_voice_lines" / f"{timestamp}"

    @classmethod
    def get_errors_path(cls) -> Path:
        return cls.ERRORS_DIR

    @classmethod
    def get_empty_content_context_path(cls) -> Path:
        return cls.ERRORS_DIR / "empty_content_context.txt"

    @classmethod
    def get_location_types_path(cls) -> Path:
        return cls.PLACES_DIR / "location_types.txt"

    @classmethod
    def get_tool_instructions_for_instructor_path(cls) -> Path:
        return cls.PROMPTING_DIR / "tool_instructions_for_instructor.txt"

    @classmethod
    def get_local_information_path(cls) -> Path:
        return cls.BLOCKS_DIR / "local_information.txt"

    @classmethod
    def get_character_information_path(cls) -> Path:
        return cls.BLOCKS_DIR / "character_information.txt"

    @classmethod
    def get_places_descriptions_path(cls) -> Path:
        return cls.BLOCKS_DIR / "places_descriptions.txt"

    @classmethod
    def get_players_and_followers_information_path(cls) -> Path:
        return cls.BLOCKS_DIR / "player_and_followers_information.txt"

    @classmethod
    def get_choosing_speech_turn_prompt_path(cls) -> Path:
        return cls.DIALOGUES_DIR / "choosing_speech_turn_prompt.txt"

    @classmethod
    def get_narrative_beat_generation_prompt_path(cls) -> Path:
        return cls.DIALOGUES_DIR / "narrative_beat_generation_prompt.txt"

    @classmethod
    def get_grow_event_prompt_path(cls) -> Path:
        return cls.DIALOGUES_DIR / "grow_event_prompt.txt"

    @classmethod
    def get_speech_turn_prompt_path(cls) -> Path:
        return cls.DIALOGUES_DIR / "speech_turn_prompt.txt"

    @classmethod
    def get_summarize_dialogue_prompt_path(cls) -> Path:
        return cls.DIALOGUES_DIR / "summarize_dialogue_prompt.txt"

    @classmethod
    def get_ambient_narration_generation_prompt_path(cls) -> Path:
        return cls.DIALOGUES_DIR / "ambient_narration_generation_prompt.txt"

    @classmethod
    def get_confrontation_round_generation_prompt_path(cls) -> Path:
        return cls.DIALOGUES_DIR / "confrontation_round_generation_prompt.txt"

    @classmethod
    def get_story_universe_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_BASE_DIR / "story_universe_generation_prompt.txt"

    @classmethod
    def get_base_character_data_generation_prompt_path(cls) -> Path:
        return (
            cls.PROMPTING_CHARACTERS_DIR / "base_character_data_generation_prompt.txt"
        )

    @classmethod
    def get_speech_patterns_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_CHARACTERS_DIR / "speech_patterns_generation_prompt.txt"

    @classmethod
    def get_self_reflection_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_CHARACTERS_DIR / "self_reflection_generation_prompt.txt"

    @classmethod
    def get_worldview_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_CHARACTERS_DIR / "worldview_generation_prompt.txt"

    @classmethod
    def get_character_generation_guidelines_prompt_path(cls) -> Path:
        return (
            cls.PROMPTING_CHARACTERS_DIR / "character_generation_guidelines_prompt.txt"
        )

    @classmethod
    def get_character_description_generation_prompt_path(cls) -> Path:
        return (
            cls.PROMPTING_CHARACTERS_DIR / "character_description_generation_prompt.txt"
        )

    @classmethod
    def get_secrets_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_CHARACTERS_DIR / "secrets_generation_prompt.txt"

    @classmethod
    def get_connection_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_CHARACTERS_DIR / "connection_generation_prompt.txt"

    @classmethod
    def get_scenarios_generation_prompt_path(cls) -> Path:
        return cls.CONCEPTS_DIR / "scenarios_generation_prompt.txt"

    @classmethod
    def get_dilemmas_generation_prompt_path(cls) -> Path:
        return cls.CONCEPTS_DIR / "dilemmas_generation_prompt.txt"

    @classmethod
    def get_plot_blueprints_generation_prompt_path(cls) -> Path:
        return cls.CONCEPTS_DIR / "plot_blueprints_generation_prompt.txt"

    @classmethod
    def get_goals_generation_prompt_path(cls) -> Path:
        return cls.CONCEPTS_DIR / "goals_generation_prompt.txt"

    @classmethod
    def get_plot_twists_generation_prompt_path(cls) -> Path:
        return cls.CONCEPTS_DIR / "plot_twists_generation_prompt.txt"

    @classmethod
    def get_world_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_PLACES_DIR / "world_generation_prompt.txt"

    @classmethod
    def get_region_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_PLACES_DIR / "region_generation_prompt.txt"

    @classmethod
    def get_area_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_PLACES_DIR / "area_generation_prompt.txt"

    @classmethod
    def get_location_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_PLACES_DIR / "location_generation_prompt.txt"

    @classmethod
    def get_place_description_prompt_path(cls) -> Path:
        return cls.PROMPTING_PLACES_DIR / "place_description_prompt.txt"

    @classmethod
    def get_travel_narration_prompt_path(cls) -> Path:
        return cls.PROMPTING_PLACES_DIR / "travel_narration_prompt.txt"

    @classmethod
    def get_image_generation_prompt_path(cls) -> Path:
        return cls.PROMPTING_IMAGES_DIR / "image_generation_prompt.txt"

    @classmethod
    def get_research_resolution_generation_prompt_path(cls) -> Path:
        return cls.ACTIONS_DIR / "research_resolution_generation_prompt.txt"

    @classmethod
    def get_investigate_resolution_generation_prompt_path(cls) -> Path:
        return cls.ACTIONS_DIR / "investigate_resolution_generation_prompt.txt"

    @classmethod
    def get_gather_supplies_resolution_generation_prompt_path(cls) -> Path:
        return cls.ACTIONS_DIR / "gather_supplies_resolution_generation_prompt.txt"

    @classmethod
    def get_templates_paths(cls, place_type: TemplateType):
        """
        Returns the path to the template file for the given type.
        """
        filename = cls.TEMPLATE_FILES.get(place_type)

        if not filename:
            raise ValueError(f"Unknown template type: {place_type}")

        return cls.TEMPLATES_DIR / filename

    @classmethod
    def get_playthroughs_path(cls) -> Path:
        return cls.PLAYTHROUGHS_DIR

    @classmethod
    def get_playthrough_path(cls, playthrough_name: str) -> Path:
        """
        Returns the path to the playthrough directory.

        Args:
            playthrough_name (str): The name of the playthrough.

        Returns:
            Path: The path to the playthrough directory.
        """
        return cls.PLAYTHROUGHS_DIR / f"{playthrough_name}"

    @classmethod
    def get_static_playthrough_path(cls, playthrough_name: str) -> Path:
        return cls.STATIC_PLAYTHROUGHS_DIR / f"{playthrough_name}"

    @classmethod
    def get_default_image_path(cls) -> Path:
        return cls.IMAGES_DIR / "default.png"

    @classmethod
    def get_playthrough_images_path(cls, playthrough_name: str) -> Path:
        return cls.get_static_playthrough_path(playthrough_name) / "images"

    @classmethod
    def get_character_image_path(
        cls, playthrough_name: str, character_identifier: str
    ) -> Path:
        return (
            cls.get_playthrough_images_path(playthrough_name)
            / f"{character_identifier}.png"
        )

    @classmethod
    def get_characters_path(cls, playthrough_name: str) -> Path:
        return cls.get_playthrough_path(playthrough_name) / "characters"

    @classmethod
    def get_concepts_path(cls, playthrough_name: str) -> Path:
        return cls.get_playthrough_path(playthrough_name) / "concepts"

    @classmethod
    def get_playthrough_metadata_path(cls, playthrough_name: str) -> Path:
        return cls.get_playthrough_path(playthrough_name) / "playthrough_metadata.json"

    @classmethod
    def get_writers_room_path(cls, playthrough_name: str):
        return cls.get_playthrough_path(playthrough_name) / "writers_room"

    @classmethod
    def get_writers_room_context_path(cls, playthrough_name: str):
        return cls.get_writers_room_path(playthrough_name) / "context.txt"

    @classmethod
    def get_writers_room_session(cls, playthrough_name: str):
        return cls.get_writers_room_path(playthrough_name) / "session.json"

    @classmethod
    def get_characters_file_path(cls, playthrough_name: str) -> Path:
        return cls.get_characters_path(playthrough_name) / "characters.json"

    @classmethod
    def get_character_path(
        cls, playthrough_name: str, character_identifier: str, character_name: str
    ) -> Path:
        return (
            cls.get_characters_path(playthrough_name)
            / f"{character_name} - {character_identifier}"
        )

    @classmethod
    def get_memories_path(
        cls, playthrough_name: str, character_identifier: str, character_name: str
    ):
        return (
            cls.get_character_path(
                playthrough_name, character_identifier, character_name
            )
            / "memories.txt"
        )

    @classmethod
    def get_dialogues_path(
        cls, playthrough_name: str, character_identifier: str, character_name: str
    ):
        return (
            cls.get_character_path(
                playthrough_name, character_identifier, character_name
            )
            / "dialogues.txt"
        )

    @classmethod
    def get_map_path(cls, playthrough_name: str) -> Path:
        return cls.get_playthrough_path(playthrough_name) / "map.json"

    @classmethod
    def get_adventure_path(cls, playthrough_name: str) -> Path:
        return cls.get_playthrough_path(playthrough_name) / "adventure.txt"

    @classmethod
    def get_concept_file_path(
        cls, playthrough_name: str, concept_type: ConceptType
    ) -> Path:
        file_name = f"{concept_type.value}.txt"
        return cls.get_concepts_path(playthrough_name) / file_name

    @classmethod
    def get_facts_path(cls, playthrough_name: str) -> Path:
        return cls.get_playthrough_path(playthrough_name) / "facts.txt"

    @classmethod
    def get_ongoing_dialogue_path(cls, playthrough_name: str) -> Path:
        return cls.get_playthrough_path(playthrough_name) / "ongoing_dialogue.json"

    @classmethod
    def get_voice_line_path(cls, character_name: str, voice_model: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}-{character_name}-{voice_model}.wav"
        return cls.VOICE_LINES_DIR / file_name
