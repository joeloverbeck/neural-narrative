from typing import List

from src.characters.abstracts.strategies import OtherCharactersIdentifiersStrategy


class ParticipantsIdentifiersStrategy(OtherCharactersIdentifiersStrategy):
    def __init__(self, participants_identifiers: List[str]):
        self._participants_identifiers = participants_identifiers

    def get_data(self) -> List[str]:
        return self._participants_identifiers
