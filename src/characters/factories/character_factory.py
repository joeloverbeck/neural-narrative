from src.characters.character import Character


class CharacterFactory:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def create_character(self, character_identifier: str):
        return Character(self._playthrough_name, character_identifier)
