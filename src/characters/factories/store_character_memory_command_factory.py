from src.characters.commands.store_character_memory_command import StoreCharacterMemoryCommand


class StoreCharacterMemoryCommandFactory:
    def __init__(self, playthrough_name: str):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")

        self._playthrough_name = playthrough_name

    def create_store_character_memory_command(self, participant_identifier: str,
                                              summary: str) -> StoreCharacterMemoryCommand:
        if not participant_identifier:
            raise ValueError("participant_identifier can't be empty.")
        if not summary:
            raise ValueError("summary can't be empty.")

        return StoreCharacterMemoryCommand(self._playthrough_name, participant_identifier, summary)
