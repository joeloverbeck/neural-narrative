from typing import Optional

from src.base.enums import IdentifierType
from src.base.factories.store_last_identifier_command_factory import (
    StoreLastIdentifierCommandFactory,
)
from src.base.identifiers_manager import IdentifiersManager
from src.base.validators import validate_non_empty_string


class ProduceAndUpdateNextIdentifierAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        identifier_type: IdentifierType,
        store_last_identifier_command_factory: StoreLastIdentifierCommandFactory,
        identifiers_manager: Optional[IdentifiersManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._identifier_type = identifier_type
        self._store_last_identifier_command_factory = (
            store_last_identifier_command_factory
        )

        self._identifiers_manager = identifiers_manager or IdentifiersManager(
            self._playthrough_name
        )

    def do_algorithm(self) -> int:
        next_identifier = self._identifiers_manager.determine_next_identifier(
            self._identifier_type
        )

        self._store_last_identifier_command_factory.create_command(
            self._identifier_type, next_identifier
        ).execute()

        return next_identifier
