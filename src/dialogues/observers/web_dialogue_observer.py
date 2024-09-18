from typing import List

from flask import session

from src.abstracts.observer import Observer
from src.characters.characters_manager import CharactersManager


class WebDialogueObserver(Observer):
    def __init__(self):
        self._messages = []
        self._characters_manager = CharactersManager(session.get("playthrough_name"))

    def update(self, message: dict) -> None:
        # alignment = 'left' if sender_id != 'player' else 'right'

        self._messages.append(
            {
                "alignment": message["alignment"],
                "sender_name": message["sender_name"],
                "sender_photo_url": message["sender_photo_url"],
                "message_text": message["message_text"],
            }
        )

    def get_messages(self) -> List[dict]:
        return self._messages
