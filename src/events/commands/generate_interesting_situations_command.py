import logging

from src.abstracts.command import Command
from src.events.factories.interesting_situations_factory import (
    InterestingSituationsFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class GenerateInterestingSituationsCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        interesting_situations_factory: InterestingSituationsFactory,
        filesystem_manager: FilesystemManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._interesting_situations_factory = interesting_situations_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:

        interesting_situations_product = (
            self._interesting_situations_factory.generate_product()
        )

        if not interesting_situations_product.is_valid():
            logger.error(
                "Was unable to generate interesting situations. Error: %s",
                interesting_situations_product.error(),
            )
            return

        if not interesting_situations_product.get():
            logger.error("No interesting situations have been generated.")
            return

        # Generated interesting situations. Must save them.
        interesting_situations = ""

        for interesting_situation in interesting_situations_product.get():
            if interesting_situation:
                interesting_situations += "\n" + interesting_situation

        self._filesystem_manager.append_to_file(
            self._filesystem_manager.get_file_path_to_interesting_situations(
                self._playthrough_name
            ),
            interesting_situations,
        )

        logger.info(
            "Generated interesting situations at '%s'",
            self._filesystem_manager.get_file_path_to_interesting_situations(
                self._playthrough_name
            ),
        )
