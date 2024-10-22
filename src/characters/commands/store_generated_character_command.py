import logging.config
from typing import Optional

from src.base.abstracts.command import Command
from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.identifiers_manager import IdentifiersManager
from src.characters.character_data import CharacterDataForStorage
from src.filesystem.filesystem_manager import FilesystemManager
from src.voices.algorithms.match_voice_data_to_voice_model_algorithm import (
    MatchVoiceDataToVoiceModelAlgorithm,
)
from src.voices.voice_attributes import VoiceAttributes

logger = logging.getLogger(__name__)


class StoreGeneratedCharacterCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        character_data: dict,
        match_voice_data_to_voice_model_algorithm: MatchVoiceDataToVoiceModelAlgorithm,
        produce_and_update_next_identifier_algorithm: ProduceAndUpdateNextIdentifierAlgorithm,
        filesystem_manager: Optional[FilesystemManager] = None,
        identifiers_manager: Optional[IdentifiersManager] = None,
    ):
        if not character_data:
            raise ValueError("character_data can't be empty.")
        if not character_data["name"]:
            raise ValueError("malformed character_data.")
        self._playthrough_name = playthrough_name
        self._match_voice_data_to_voice_model_algorithm = (
            match_voice_data_to_voice_model_algorithm
        )
        self._produce_and_update_next_identifier_algorithm = (
            produce_and_update_next_identifier_algorithm
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            self._playthrough_name
        )
        try:
            self._character_data = CharacterDataForStorage(
                character_data["name"],
                character_data["description"],
                character_data["personality"],
                character_data["profile"],
                character_data["likes"],
                character_data["dislikes"],
                character_data["secrets"],
                character_data["speech_patterns"],
                character_data["health"],
                character_data["equipment"],
                character_data["voice_gender"],
                character_data["voice_age"],
                character_data["voice_emotion"],
                character_data["voice_tempo"],
                character_data["voice_volume"],
                character_data["voice_texture"],
                character_data["voice_tone"],
                character_data["voice_style"],
                character_data["voice_personality"],
                character_data["voice_special_effects"],
            )
        except ValueError as e:
            raise ValueError(f"Invalid character_data: {e}")

    def execute(self) -> None:
        characters_file = self._filesystem_manager.get_file_path_to_characters_file(
            self._playthrough_name
        )
        characters = self._filesystem_manager.load_existing_or_new_json_file(
            characters_file
        )
        modified_character_data = {
            "name": self._character_data.name,
            "description": self._character_data.description,
            "personality": self._character_data.personality,
            "profile": self._character_data.profile,
            "likes": self._character_data.likes,
            "dislikes": self._character_data.dislikes,
            "secrets": self._character_data.secrets,
            "speech_patterns": self._compose_speech_patterns(),
            "health": self._character_data.health,
            "equipment": self._character_data.equipment,
            "voice_gender": self._character_data.voice_gender,
            "voice_age": self._character_data.voice_age,
            "voice_emotion": self._character_data.voice_emotion,
            "voice_tempo": self._character_data.voice_tempo,
            "voice_volume": self._character_data.voice_volume,
            "voice_texture": self._character_data.voice_texture,
            "voice_tone": self._character_data.voice_tone,
            "voice_style": self._character_data.voice_style,
            "voice_personality": self._character_data.voice_personality,
            "voice_special_effects": self._character_data.voice_special_effects,
            "voice_model": self._match_voice_data_to_voice_model_algorithm.match(
                VoiceAttributes(
                    self._character_data.voice_gender,
                    self._character_data.voice_age,
                    self._character_data.voice_emotion,
                    self._character_data.voice_tempo,
                    self._character_data.voice_volume,
                    self._character_data.voice_texture,
                    self._character_data.voice_tone,
                    self._character_data.voice_style,
                    self._character_data.voice_personality,
                    self._character_data.voice_special_effects,
                )
            ),
        }
        characters[
            self._produce_and_update_next_identifier_algorithm.do_algorithm()
        ] = modified_character_data
        self._filesystem_manager.save_json_file(characters, characters_file)
        logger.info(
            f"Saved character '{self._character_data.name}' at '{characters_file}'."
        )

    def _compose_speech_patterns(self) -> str:
        speech_patterns = ""
        for pattern in self._character_data.speech_patterns:
            speech_patterns += f"{self._character_data.name}: {pattern}\n"
        return speech_patterns.strip()
