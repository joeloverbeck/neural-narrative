from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)


class CharacterInformationProviderFactory:
    def __init__(self, playthrough_name: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name

    def create_provider(self, character_identifier: str):
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")

        return CharacterInformationProvider(
            self._playthrough_name, character_identifier
        )
