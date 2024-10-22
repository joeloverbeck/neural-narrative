import logging
from typing import Optional, cast

from src.base.abstracts.command import Command
from src.base.constants import STORY_UNIVERSES_TEMPLATE_FILE
from src.base.exceptions import StoryUniverseGenerationError
from src.base.factories.story_universe_factory import StoryUniverseFactory
from src.base.products.story_universe_product import StoryUniverseProduct
from src.base.validators import validate_non_empty_string
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class GenerateStoryUniverseCommand(Command):

    def __init__(
        self,
        story_universe_factory: StoryUniverseFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._story_universe_factory = story_universe_factory
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        try:
            product = cast(
                StoryUniverseProduct, self._story_universe_factory.generate_product()
            )
        except ValueError as e:
            error_message = f"Failed to generate a story universe. Error: {e}"
            logger.error(error_message)
            raise StoryUniverseGenerationError(error_message) from e
        story_universes_file = self._filesystem_manager.load_existing_or_new_json_file(
            STORY_UNIVERSES_TEMPLATE_FILE
        )

        product_name = product.get_name()

        validate_non_empty_string(product_name, "product name")

        story_universes_file[product_name] = {
            "description": product.get_description(),
            "categories": [category for category in product.get_categories()],
        }
        self._filesystem_manager.save_json_file(
            story_universes_file, STORY_UNIVERSES_TEMPLATE_FILE
        )
        logger.info("Saved story universe '%s'.", product.get_name())
