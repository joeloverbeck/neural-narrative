from src.base.algorithms.produce_and_update_next_identifier_algorithm import (
    ProduceAndUpdateNextIdentifierAlgorithm,
)
from src.base.enums import IdentifierType
from src.base.factories.store_last_identifier_command_factory import (
    StoreLastIdentifierCommandFactory,
)
from src.base.validators import validate_non_empty_string
from src.maps.factories.create_map_entry_for_playthrough_command_provider_factory import (
    CreateMapEntryForPlaythroughCommandProviderFactory,
)


class CreateMapEntryForPlaythroughCommandProviderFactoryComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def create_factory(self) -> CreateMapEntryForPlaythroughCommandProviderFactory:
        store_last_identifier_command_factory = StoreLastIdentifierCommandFactory(
            self._playthrough_name
        )

        produce_and_update_next_identifier = ProduceAndUpdateNextIdentifierAlgorithm(
            self._playthrough_name,
            IdentifierType.PLACES,
            store_last_identifier_command_factory,
        )

        return CreateMapEntryForPlaythroughCommandProviderFactory(
            self._playthrough_name, produce_and_update_next_identifier
        )
