from typing import List


class Participants:

    def __init__(self):
        self._participants: dict = {}

    def get(self):
        return self._participants

    def add_participant(self, identifier: str, name: str, description: str, personality: str, equipment: str):
        if not identifier:
            raise ValueError("identifier must not be empty.")
        if not isinstance(identifier, str):
            raise ValueError(f"Identifier must be string, but it was {type(identifier)}.")

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

        # Correct way to update the dictionary
        self._participants[identifier] = {"name": name, "description": description, "personality": personality,
                                          "equipment": equipment}

    def enough_participants(self):
        return self.number_of_participants() >= 2

    def number_of_participants(self) -> int:
        return len(self._participants)

    def get_participant_keys(self) -> List[str]:
        """Return a list of the string keys from the internal dictionary."""
        return list(self._participants.keys())
