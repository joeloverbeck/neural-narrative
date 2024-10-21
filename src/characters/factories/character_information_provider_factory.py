from src.base.required_string import RequiredString
from src.characters.factories.character_information_provider import (
    CharacterInformationProvider,
)


class CharacterInformationProviderFactory:
    def __init__(self, playthrough_name: RequiredString):
        self._playthrough_name = playthrough_name

    def create_provider(self, character_identifier: RequiredString):
        return CharacterInformationProvider(
            self._playthrough_name, character_identifier
        )
