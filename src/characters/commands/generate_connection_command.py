from typing import cast

from src.base.abstracts.command import Command
from src.characters.factories.connection_factory import ConnectionFactory
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.characters.products.connection_product import ConnectionProduct


class GenerateConnectionCommand(Command):
    def __init__(
        self,
        character_a_identifier: str,
        character_b_identifier: str,
        connection_factory: ConnectionFactory,
        store_character_memory_command_factory: StoreCharacterMemoryCommandFactory,
    ):
        if not character_a_identifier:
            raise ValueError("character_a_identifier can't be empty.")
        if not character_b_identifier:
            raise ValueError("character_b_identifier can't be empty.")

        self._character_a_identifier = character_a_identifier
        self._character_b_identifier = character_b_identifier
        self._connection_factory = connection_factory
        self._store_character_memory_command_factory = (
            store_character_memory_command_factory
        )

    def execute(self) -> None:
        product = cast(ConnectionProduct, self._connection_factory.generate_product())

        if not product.is_valid():
            raise ValueError(
                f"Failed to generate a valid connection between characters. Error: {product.get_error()}"
            )

        # At this point, the connection is valid. Insert it as a memory for both characters.
        self._store_character_memory_command_factory.create_store_character_memory_command(
            self._character_a_identifier, product.get()
        ).execute()

        self._store_character_memory_command_factory.create_store_character_memory_command(
            self._character_b_identifier, product.get()
        ).execute()
