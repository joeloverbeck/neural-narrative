import os
from typing import List

from flask import url_for

from src.characters.character import Character


class WebService:
    @staticmethod
    def format_image_urls_of_characters(characters: List[Character]):
        for character in characters:
            character.update_data(
                {"image_url": url_for("static", filename=character.image_url)}
            )

    @staticmethod
    def get_file_url(folder: str, file_name: str):
        if not folder:
            raise ValueError("folder can't be empty.")
        if not file_name:
            raise ValueError("file_name can't be empty.")

        return url_for("static", filename=f"{folder}/" + os.path.basename(file_name))

    @staticmethod
    def create_method_name(action: str):
        if not action:
            raise ValueError("action can't be empty.")

        return f"handle_{action.replace(' ', '_').lower()}"
