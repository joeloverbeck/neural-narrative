import logging
from typing import cast, Optional

from src.base.required_string import RequiredString
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.characters.factories.self_reflection_factory import SelfReflectionFactory
from src.characters.products.produce_self_reflection_product import (
    ProduceSelfReflectionProduct,
)
from src.characters.products.self_reflection_product import SelfReflectionProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)

logger = logging.getLogger(__name__)


class ProduceSelfReflectionAlgorithm:
    def __init__(
        self,
        playthrough_name: RequiredString,
        character_identifier: RequiredString,
        self_reflection_factory: SelfReflectionFactory,
        direct_voice_line_generation_algorithm_factory: DirectVoiceLineGenerationAlgorithmFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
        characters_manager: Optional[CharactersManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._self_reflection_factory = self_reflection_factory
        self._direct_voice_line_generation_algorithm_factory = (
            direct_voice_line_generation_algorithm_factory
        )

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )

    def do_algorithm(self) -> ProduceSelfReflectionProduct:
        product = cast(
            SelfReflectionProduct, self._self_reflection_factory.generate_product()
        )

        if not product.is_valid():
            raise ValueError(
                f"Failed to generate the self-reflection. Error: {product.get_error()}"
            )

        # Character data
        character = Character(self._playthrough_name, self._character_identifier)

        # Append the memory to the existing memories.
        self._filesystem_manager.append_to_file(
            self._filesystem_manager.get_file_path_to_character_memories(
                self._playthrough_name,
                self._character_identifier,
                character.name,
            ),
            RequiredString("\n" + product.get().value),
        )

        voice_line_file_name = (
            self._direct_voice_line_generation_algorithm_factory.create_algorithm(
                character.name, product.get(), character.voice_model
            ).direct_voice_line_generation()
        )

        logger.info("Generated the self-reflection.")

        return ProduceSelfReflectionProduct(product.get(), voice_line_file_name)
