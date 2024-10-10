import logging
from typing import Optional

from src.abstracts.command import Command
from src.events.factories.concepts_factory import ConceptsFactory
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class GenerateConceptsCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        concepts_factory: ConceptsFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._concepts_factory = concepts_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:
        product = self._concepts_factory.generate_product()

        if not product.is_valid():
            logger.error("Failed to generate concepts. Error: %s", product.get_error())
            return

        prettified_concepts = ""

        for concept in product.get():
            prettified_concepts += "\n" + concept

        # Got the concepts, now have to save them.
        self._filesystem_manager.append_to_file(
            self._filesystem_manager.get_file_path_to_concepts(self._playthrough_name),
            prettified_concepts,
        )

        logger.info("Saved concepts.")
