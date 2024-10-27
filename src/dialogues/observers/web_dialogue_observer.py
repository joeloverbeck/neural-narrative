from typing import List

from flask import session

from src.base.abstracts.observer import Observer
from src.characters.characters_manager import CharactersManager
from src.services.web_service import WebService
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class WebDialogueObserver(Observer):

    def __init__(self):
        self._messages = []
        self._characters_manager = CharactersManager(session.get("playthrough_name"))

    def update(self, message: dict) -> None:
        file_name = DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
            message["sender_name"], message["message_text"], message["voice_model"]
        ).direct_voice_line_generation()

        file_url = None

        if file_name:
            file_url = WebService.get_file_url("voice_lines", file_name)

        self._messages.append(
            {
                "alignment": message["alignment"],
                "sender_name": message["sender_name"],
                "sender_photo_url": message["sender_photo_url"],
                "message_text": message["message_text"],
                "file_url": file_url,
            }
        )

    def get_messages(self) -> List[dict]:
        return self._messages
