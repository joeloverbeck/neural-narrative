import logging
from typing import cast, Optional

from src.base.products.text_product import TextProduct
from src.characters.factories.worldview_factory import WorldviewFactory
from src.characters.models.worldview import Worldview
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

        logger.info("Generated the worldview.")

        return product
