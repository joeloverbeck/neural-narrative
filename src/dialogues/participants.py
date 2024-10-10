from typing import List, Optional


class Participants:

    def __init__(self):
        self._participants: dict = {}

    def get(self):
        return self._participants

    def add_participant(
        self,
        identifier: str,
        name: str,
        description: str,
        personality: str,
        equipment: str,
        voice_model: str,
    ):
        if not identifier:
            raise ValueError("identifier must not be empty.")
        if not isinstance(identifier, str):
            raise ValueError(
                f"Identifier must be string, but it was {type(identifier)}."
            )

        # Check if the identifier can be converted to an int
        try:
            int(identifier)
        except ValueError:
            raise ValueError("identifier must be convertible to an integer.")

        if not name:
            raise ValueError("name must not be empty.")
        if not description:
            raise ValueError("description must not be empty.")
        if not personality:
            raise ValueError("personality must not be empty.")
        if not equipment:
            raise ValueError("equipment must not be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")

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

    def get_participant_keys(self) -> List[str]:
        """Return a list of the string keys from the internal dictionary."""
        return list(self._participants.keys())

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