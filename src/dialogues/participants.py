import logging
from typing import List, Optional

from src.base.required_string import RequiredString

logger = logging.getLogger(__name__)


class Participants:

    def __init__(self):
        self._participants: dict = {}

    def get(self):
        return self._participants

    def add_participant(
        self,
        identifier: RequiredString,
        name: RequiredString,
        description: RequiredString,
        personality: RequiredString,
        equipment: RequiredString,
        voice_model: RequiredString,
    ):
        # Check if the identifier can be converted to an int
        try:
            int(identifier.value)
        except ValueError:
            raise ValueError("identifier must be convertible to an integer.")

        # I fund a bug in which the description received the value of name. Protect against that.
        if name == description:
            logger.error(
                f"Attempted to add a participant with a name equal to the description. Data: {identifier} | {name} | {personality} | {equipment} | {voice_model}"
            )
            raise ValueError(
                "Attempted to add a participant for whom the name was equal to the description."
            )

        # Correct way to update the dictionary
        self._participants[identifier] = {
            "name": name,
            "description": description,
            "personality": personality,
            "equipment": equipment,
            "voice_model": voice_model,
        }

    def enough_participants(self):
        return self.number_of_participants() >= 2

    def number_of_participants(self) -> int:
        return len(self._participants)

    def get_participant_keys(self) -> List[RequiredString]:
        """Return a list of the string keys from the internal dictionary."""
        return list(RequiredString(key) for key in self._participants.keys())

    def has_only_two_participants_with_player(self, player_identifier: str) -> bool:
        """
        Check if there are only two participants and one of them is the player's identifier.
        """
        return len(self._participants) == 2 and player_identifier in self._participants

    def get_other_participant_data(self, player_identifier: str) -> Optional[dict]:
        """
        Return the other participant's data if there are only two participants,
        and one of them is the player's identifier.
        """
        if not self.has_only_two_participants_with_player(player_identifier):
            return None
        for identifier in self._participants:
            if identifier != player_identifier:
                return {
                    "identifier": identifier,
                    "name": self._participants[identifier]["name"],
                    "voice_model": self._participants[identifier]["voice_model"],
                }
