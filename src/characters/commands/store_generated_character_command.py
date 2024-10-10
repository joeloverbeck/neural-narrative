import logging
import logging.config

from src.abstracts.command import Command
from src.enums import IdentifierType
from src.filesystem.filesystem_manager import FilesystemManager
from src.identifiers_manager import IdentifiersManager
from src.voices.algorithms.match_voice_data_to_voice_model_algorithm import (
    MatchVoiceDataToVoiceModelAlgorithm,
)

logger = logging.getLogger(__name__)


class StoreGeneratedCharacterCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_data: dict,
        match_voice_data_to_voice_model_algorithm: MatchVoiceDataToVoiceModelAlgorithm,
        filesystem_manager: FilesystemManager = None,
        identifiers_manager: IdentifiersManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not character_data:
            raise ValueError("character_data can't be empty.")
        if not character_data["name"]:
            raise ValueError("malformed character_data.")

        self._playthrough_name = playthrough_name
        self._character_data = character_data
        self._match_voice_data_to_voice_model_algorithm = (
            match_voice_data_to_voice_model_algorithm
        )

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            self._playthrough_name
        )

        logging.config.dictConfig(self._filesystem_manager.get_logging_config_file())

    def execute(self) -> None:
        # Build the path to the characters.json file
        filesystem_manager = FilesystemManager()

        characters_file = filesystem_manager.get_file_path_to_characters_file(
            self._playthrough_name
        )

        characters = filesystem_manager.load_existing_or_new_json_file(characters_file)

        modified_character_data = {
            "name": self._character_data["name"],
            "description": self._character_data["description"],
            "personality": self._character_data["personality"],
            "profile": self._character_data["profile"],
            "likes": self._character_data["likes"],
            "dislikes": self._character_data["dislikes"],
            "first message": self._character_data["first message"],
            "speech patterns": self._compose_speech_patterns(),
            "health": self._character_data["health"],
            "equipment": self._character_data["equipment"],
            "voice_gender": self._character_data["voice_gender"],
            "voice_age": self._character_data["voice_age"],
            "voice_emotion": self._character_data["voice_emotion"],
            "voice_tempo": self._character_data["voice_tempo"],
            "voice_volume": self._character_data["voice_volume"],
            "voice_texture": self._character_data["voice_texture"],
            "voice_tone": self._character_data["voice_tone"],
            "voice_style": self._character_data["voice_style"],
            "voice_personality": self._character_data["voice_personality"],
            "voice_special_effects": self._character_data["voice_special_effects"],
            "voice_model": self._match_voice_data_to_voice_model_algorithm.match(
                self._character_data
            ),
        }

        # Add the new character entry
        characters[
            self._identifiers_manager.produce_and_update_next_identifier(
                IdentifierType.CHARACTERS
            )
        ] = modified_character_data

        filesystem_manager.save_json_file(characters, characters_file)

        logger.info(
            f"Saved character '{self._character_data["name"]}' at '{characters_file}'"
        )

    def _compose_speech_patterns(self):
        speech_patterns = (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_1"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_2"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_3"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_4"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_5"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_6"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_7"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_8"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_9"]
            + "\n"
        )
        speech_patterns += (
            self._character_data["name"]
            + ": "
            + self._character_data["speech_pattern_10"]
        )
        return speech_patterns
