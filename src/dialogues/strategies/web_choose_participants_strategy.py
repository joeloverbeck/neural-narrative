from typing import List

from src.base.validators import validate_list_of_str


class WebChooseParticipantsStrategy:

    def __init__(self, chosen_participants: List[str]):
        validate_list_of_str(chosen_participants)

        self._chosen_participants = chosen_participants

    def choose_participants(self) -> List[str]:
        return self._chosen_participants
