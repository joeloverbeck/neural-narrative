from typing import cast, Optional

from src.abstracts.command import Command
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.factories.secrets_factory import SecretsFactory
from src.characters.products.secrets_product import SecretsProduct


class GenerateCharacterSecretsCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        secrets_factory: SecretsFactory,
        characters_manager: Optional[CharactersManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._secrets_factory = secrets_factory

        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def execute(self) -> None:
        product = cast(SecretsProduct, self._secrets_factory.generate_product())

        if not product.is_valid():
            raise ValueError(
                f"Was unable to generate secrets. Error: {product.get_error()}"
            )

        character = Character(self._playthrough_name, self._character_identifier)

        character.update_data({"secrets": product.get()})

        # Must store the secrets.
        character.save()