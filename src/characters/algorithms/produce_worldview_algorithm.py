import logging
from typing import cast, Optional

from src.base.products.text_product import TextProduct
from src.characters.character import Character
from src.characters.factories.worldview_factory import WorldviewFactory
from src.characters.models.worldview import Worldview
from src.filesystem.file_operations import append_to_file
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class ProduceWorldviewAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        worldview_factory: WorldviewFactory,
        path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character_identifier = character_identifier
        self._worldview_factory = worldview_factory

        self._path_manager = path_manager or PathManager()

    def do_algorithm(self) -> TextProduct:
        product = cast(
            TextProduct,
            self._worldview_factory.generate_product(Worldview),
        )

        if not product.is_valid():
            raise ValueError(
                f"Failed to generate the worldview. Error: {product.get_error()}"
            )

        character = Character(self._playthrough_name, self._character_identifier)

        append_to_file(
            self._path_manager.get_memories_path(
                self._playthrough_name, character.identifier, character.name
            ),
            "\n" + product.get(),
        )

        logger.info("Generated the worldview.")

        return product
