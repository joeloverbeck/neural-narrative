import os
from typing import List

from flask import session, url_for

from src.abstracts.observer import Observer
from src.characters.characters_manager import CharactersManager
from src.services.voices_services import VoicesServices


class WebDialogueObserver(Observer):
    def __init__(self):
        self._messages = []
        self._characters_manager = CharactersManager(session.get("playthrough_name"))

    def update(self, message: dict) -> None:
        # Generate the voice line and get the file path
        file_name = VoicesServices().generate_voice_line(
            message["sender_name"], message["message_text"], message["voice_model"]
        )

        # Could be that file_name is None, in case the pod isn't running.
        file_url = None

        if file_name:
            file_url = url_for(
                "static", filename="voice_lines/" + os.path.basename(file_name)
            )

        # Append the message with the file path
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
