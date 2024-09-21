from src.characters.commands.store_generated_character_command import (
    StoreGeneratedCharacterCommand,
)


class StoreGeneratedCharacterCommandFactory:

    def __init__(self, playthrough_name: str):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name

    def create_store_generated_character_command(
        self, character_data: dict
    ) -> StoreGeneratedCharacterCommand:
        return StoreGeneratedCharacterCommand(self._playthrough_name, character_data)
