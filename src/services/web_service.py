from typing import List

from flask import url_for


class WebService:
    @staticmethod
    def format_image_urls_of_characters(characters: List[dict]):
        for character in characters:
            character["image_url"] = url_for("static", filename=character["image_url"])

    @staticmethod
    def create_method_name(action: str):
        if not action:
            raise ValueError("action can't be empty.")

        return f"handle_{action.replace(' ', '_').lower()}"
