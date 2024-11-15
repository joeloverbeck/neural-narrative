import logging
from typing import cast, Optional

from src.base.products.text_product import TextProduct
from src.characters.character import Character
from src.characters.factories.self_reflection_factory import SelfReflectionFactory
from src.characters.models.self_reflection import SelfReflection
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class ProduceSelfReflectionAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        character: Character,
        self_reflection_factory: SelfReflectionFactory,
        path_manager: Optional[PathManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._character = character
        self._self_reflection_factory = self_reflection_factory

        self._path_manager = path_manager or PathManager()

    def do_algorithm(self) -> TextProduct:
        product = cast(
            TextProduct,
            self._self_reflection_factory.generate_product(SelfReflection),
        )

        if not product.is_valid():
            raise ValueError(
                f"Failed to generate the self-reflection. Error: {product.get_error()}"
            )

        logger.info("Generated the self-reflection.")

        return TextProduct(product.get(), is_valid=True)
