from typing import List


class WebChooseParticipantsStrategy:

    def __init__(self, chosen_participants: List[str]):
        self._chosen_participants = chosen_participants

    def choose_participants(self) -> List[str]:
        return self._chosen_participants
