from typing import List

from src.base.required_string import RequiredString


class WebChooseParticipantsStrategy:
    def __init__(self, chosen_participants: List[RequiredString]):
        self._chosen_participants = chosen_participants

    def choose_participants(self) -> List[RequiredString]:
        return self._chosen_participants
