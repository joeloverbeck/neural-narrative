from src.base.commands.store_last_identifier_command import StoreLastIdentifierCommand
from src.base.enums import IdentifierType
from src.base.validators import validate_non_empty_string


class StoreLastIdentifierCommandFactory:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def create_command(
        self, identifier_type: IdentifierType, next_identifier: int
    ) -> StoreLastIdentifierCommand:
        return StoreLastIdentifierCommand(
            self._playthrough_name, identifier_type, next_identifier
        )
