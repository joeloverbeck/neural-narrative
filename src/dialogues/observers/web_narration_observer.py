from pathlib import Path
from typing import List, Optional

from flask import session

from src.base.abstracts.observer import Observer
from src.characters.characters_manager import CharactersManager
from src.filesystem.config_loader import ConfigLoader
from src.services.web_service import WebService
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class WebNarrationObserver(Observer):

    def __init__(self, config_loader: Optional[ConfigLoader] = None):
        self._messages = []
        self._characters_manager = CharactersManager(session.get("playthrough_name"))

        self._config_loader = config_loader or ConfigLoader()

    def update(self, message: dict) -> None:
        if not "alignment" in message:
            raise KeyError(f"Expected 'alignment' to be in message, but was: {message}")

        if not "message_text" in message:
            raise KeyError(
                f"Expected 'message_text' to be in message, but was: {message}"
            )

        if not "message_type" in message:
            raise KeyError(
                f"Expected 'message_type' to be in message, but was: {message}"
            )

        file_name = DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
            "narrator",
            message["message_text"],
            self._config_loader.get_narrator_voice_model(),
        ).direct_voice_line_generation()

        file_url = None

        if file_name:
            file_url = WebService.get_file_url(Path("voice_lines"), file_name)

        self._messages.append(
            {
                "alignment": message["alignment"],
                "message_text": message["message_text"],
                "message_type": message["message_type"],
                "file_url": file_url,
            }
        )

    def get_messages(self) -> List[dict]:
        return self._messages
