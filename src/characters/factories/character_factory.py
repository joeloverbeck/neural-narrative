from src.base.required_string import RequiredString
from src.characters.character import Character


class CharacterFactory:

    def __init__(self, playthrough_name: RequiredString):
        self._playthrough_name = playthrough_name

    def create_character(self, character_identifier: RequiredString):
        return Character(self._playthrough_name, character_identifier)
