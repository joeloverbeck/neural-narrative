from src.characters.factories.character_description_provider_factory import (
    CharacterDescriptionProviderFactory,
)
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.images.commands.generate_character_image_command import (
    GenerateCharacterImageCommand,
)
from src.requests.abstracts.abstract_factories import UrlContentFactory


class GenerateCharacterImageCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        character_description_provider_factory: CharacterDescriptionProviderFactory,
        generated_image_factory: GeneratedImageFactory,
        url_content_factory: UrlContentFactory,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._character_description_provider_factory = (
            character_description_provider_factory
        )
        self._generated_image_factory = generated_image_factory
        self._url_content_factory = url_content_factory

    def create_generate_character_image_command(
        self, character_identifier: str
    ) -> GenerateCharacterImageCommand:
        if not character_identifier:
            raise ValueError("character_identifier can't be empty.")
        return GenerateCharacterImageCommand(
            self._playthrough_name,
            character_identifier,
            self._character_description_provider_factory,
            self._generated_image_factory,
            self._url_content_factory,
        )
