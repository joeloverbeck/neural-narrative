from typing import List

from flask import session

from src.abstracts.observer import Observer
from src.characters.characters_manager import CharactersManager


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

        self._messages.append(
            {
                "alignment": message["alignment"],
                "message_text": message["message_text"],
            }
        )

    def get_messages(self) -> List[dict]:
        return self._messages
