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


class WebDialogueObserver(Observer):

    def __init__(self, config_loader: Optional[ConfigLoader] = None):
        self._messages = []
        self._characters_manager = CharactersManager(session.get("playthrough_name"))

        self._config_loader = config_loader or ConfigLoader()

    def _determine_filename(self, message: dict):
        alignment = message["alignment"]

        filename = None

        if (
            self._config_loader.get_produce_player_voice_lines()
            and alignment == "right"
        ) or alignment == "left":
            filename = DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
                message["sender_name"], message["message_text"], message["voice_model"]
            ).direct_voice_line_generation()

        return filename

    @staticmethod
    def _determine_file_url(filename: Optional[Path]):
        file_url = None

        if filename:
            file_url = WebService.get_file_url(Path("voice_lines"), filename)

        return file_url

    @staticmethod
    def _format_thoughts(message: dict):
        thoughts = message.get("thoughts", "")

        return f"\n\n{thoughts}" if thoughts else ""

    @staticmethod
    def _format_desired_action(message: dict):
        desired_action = message.get("desired_action", "")

        return f"\n\n{desired_action}" if desired_action else ""

    def update(self, message: dict) -> None:
        filename = self._determine_filename(message)

        self._messages.append(
            {
                "alignment": message["alignment"],
                "sender_identifier": message.get("sender_identifier", ""),
                "sender_name": message["sender_name"],
                "sender_photo_url": message["sender_photo_url"],
                "message_text": message["message_text"],
                "thoughts": self._format_thoughts(message),
                "desired_action": self._format_desired_action(message),
                "file_url": self._determine_file_url(filename),
            }
        )

    def get_messages(self) -> List[dict]:
        return self._messages
