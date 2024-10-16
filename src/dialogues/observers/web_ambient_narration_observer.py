import os
from typing import List

from flask import session, url_for

from src.abstracts.observer import Observer
from src.characters.characters_manager import CharactersManager
from src.constants import NARRATOR_VOICE_MODEL
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


class WebAmbientNarrationObserver(Observer):
    def __init__(self):
        self._messages = []
        self._characters_manager = CharactersManager(session.get("playthrough_name"))

    def update(self, message: dict) -> None:
        if not "alignment" in message:
            raise ValueError(
                f"Expected 'alignment' to be in message, but was: {message}"
            )
        if not "message_text" in message:
            raise ValueError(
                f"Expected 'message_text' to be in message, but was: {message}"
            )

        # Generate the voice line and get the file path
        file_name = DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
            "narrator", message["message_text"], NARRATOR_VOICE_MODEL
        ).direct_voice_line_generation()

        # Append the message with the file path
        self._messages.append(
            {
                "alignment": message["alignment"],
                "message_text": message["message_text"],
                "file_url": url_for(
                    "static", filename="voice_lines/" + os.path.basename(file_name)
                ),
            }
        )

    def get_messages(self) -> List[dict]:
        return self._messages
