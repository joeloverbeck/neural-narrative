import logging
from typing import cast, Optional

from src.base.products.text_and_voice_line_url_product import TextAndVoiceLineUrlProduct
from src.base.products.text_product import TextProduct
from src.characters.character import Character
from src.characters.factories.self_reflection_factory import SelfReflectionFactory
from src.characters.models.self_reflection import SelfReflection
from src.filesystem.file_operations import append_to_file
from src.filesystem.path_manager import PathManager
from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)

logger = logging.getLogger(__name__)


class ProduceSelfReflectionAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        self_reflection_factory: SelfReflectionFactory,
        direct_voice_line_generation_algorithm_factory: DirectVoiceLineGenerationAlgorithmFactory,
        path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._self_reflection_factory = self_reflection_factory
        self._direct_voice_line_generation_algorithm_factory = (
            direct_voice_line_generation_algorithm_factory
        )

        self._path_manager = path_manager or PathManager()

    def do_algorithm(self) -> TextAndVoiceLineUrlProduct:
        product = cast(
            TextProduct,
            self._self_reflection_factory.generate_product(SelfReflection),
        )

        if not product.is_valid():
            raise ValueError(
                f"Failed to generate the self-reflection. Error: {product.get_error()}"
            )

        character = Character(self._playthrough_name, self._character_identifier)

        append_to_file(
            self._path_manager.get_memories_path(
                self._playthrough_name, character.identifier, character.name
            ),
            "\n" + product.get(),
        )

        voice_line_file_name = (
            self._direct_voice_line_generation_algorithm_factory.create_algorithm(
                character.name, product.get(), character.voice_model
            ).direct_voice_line_generation()
        )

        logger.info("Generated the self-reflection.")

        return TextAndVoiceLineUrlProduct(product.get(), voice_line_file_name)
