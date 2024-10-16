import logging
from typing import Dict, Optional

from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class Character:
    REQUIRED_ATTRIBUTES = [
        "name",
        "description",
        "personality",
        "profile",
        "likes",
        "dislikes",
        "secrets",
        "speech_patterns",
        "health",
        "equipment",
        "voice_gender",
        "voice_age",
        "voice_emotion",
        "voice_tempo",
        "voice_volume",
        "voice_tone",
        "voice_texture",
        "voice_style",
        "voice_personality",
        "voice_special_effects",
        "voice_model",
    ]

    ALLOWED_UPDATE_FIELDS = set(
        REQUIRED_ATTRIBUTES + ["description_for_portrait", "image_url"]
    )

    def __init__(
        self,
        playthrough_name: str,
        identifier: str,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name should not be empty.")
        if not identifier:
            raise ValueError("identifier should not be empty.")

        self.playthrough_name = playthrough_name
        self._identifier = identifier
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._data = self._load_character_data()
        self._validate_required_attributes()

    def _load_character_data(self) -> Dict[str, str]:
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(
                self.playthrough_name
            )
        )

        if self._identifier not in characters_file:
            raise KeyError(f"Character with identifier '{self._identifier}' not found.")

        return characters_file[self._identifier]

    def _validate_required_attributes(self):
        missing_attributes = [
            attr for attr in self.REQUIRED_ATTRIBUTES if attr not in self._data
        ]
        if missing_attributes:
            raise KeyError(
                f"Character '{self._identifier}' is missing the following required attributes: {', '.join(missing_attributes)}."
            )

    def save(self):
        characters_file = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_characters_file(
                self.playthrough_name
            )
        )

        characters_file[self._identifier] = self._data

        self._filesystem_manager.save_json_file(
            characters_file,
            self._filesystem_manager.get_file_path_to_characters_file(
                self.playthrough_name
            ),
        )

    def update_data(self, updated_data: Dict[str, str]):
        if not updated_data:
            raise ValueError("updated_data can't be empty.")

        for key, value in updated_data.items():
            if key in self.ALLOWED_UPDATE_FIELDS:
                self._data[key] = value
            else:
                logger.warning(
                    f"Ignored character attribute '{key}' during update for character {self._data["name"]}."
                )
                pass

        self.save()

    def get_attribute(self, attr: str):
        return self._data.get(attr)

    @property
    def image_url(self) -> str:
        return self._filesystem_manager.get_file_path_to_character_image_for_web(
            self.playthrough_name, self._identifier
        )

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def description(self) -> str:
        return self._data["description"]

    @property
    def personality(self) -> str:
        return self._data["personality"]

    @property
    def profile(self) -> str:
        return self._data["profile"]

    @property
    def likes(self) -> str:
        return self._data["likes"]

    @property
    def dislikes(self) -> str:
        return self._data["dislikes"]

    @property
    def secrets(self) -> str:
        return self._data["secrets"]

    @property
    def speech_patterns(self) -> str:
        return self._data["speech_patterns"]

    @property
    def health(self) -> str:
        return self._data["health"]

    @property
    def equipment(self) -> str:
        return self._data["equipment"]

    @property
    def voice_gender(self) -> str:
        return self._data["voice_gender"]

    @property
    def voice_age(self) -> str:
        return self._data["voice_age"]

    @property
    def voice_emotion(self) -> str:
        return self._data["voice_emotion"]

    @property
    def voice_tempo(self) -> str:
        return self._data["voice_tempo"]

    @property
    def voice_volume(self) -> str:
        return self._data["voice_volume"]

    @property
    def voice_tone(self) -> str:
        return self._data["voice_tone"]

    @property
    def voice_texture(self) -> str:
        return self._data["voice_texture"]

    @property
    def voice_style(self) -> str:
        return self._data["voice_style"]

    @property
    def voice_personality(self) -> str:
        return self._data["voice_personality"]

    @property
    def voice_special_effects(self) -> str:
        return self._data["voice_special_effects"]

    @property
    def voice_model(self) -> str:
        return self._data["voice_model"]

    def has_description_for_portrait(self) -> bool:
        return bool(self._data.get("description_for_portrait"))

    @property
    def description_for_portrait(self) -> str:
        return self._data["description_for_portrait"]
