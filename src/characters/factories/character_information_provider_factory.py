from src.characters.factories.character_information_provider import CharacterInformationProvider


class CharacterInformationProviderFactory:

    def __init__(self, playthrough_name: str):
        self._playthrough_name = playthrough_name

    def create_provider(self, character_identifier: str):
        return CharacterInformationProvider(self._playthrough_name,
                                            character_identifier)
