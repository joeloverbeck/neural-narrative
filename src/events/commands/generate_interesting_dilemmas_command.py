import logging
from typing import Optional

from src.abstracts.command import Command
from src.events.factories.interesting_dilemmas_factory import InterestingDilemmasFactory
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class GenerateInterestingDilemmasCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        interesting_dilemmas_factory: InterestingDilemmasFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._interesting_dilemmas_factory = interesting_dilemmas_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:

        interesting_dilemmas_product = (
            self._interesting_dilemmas_factory.generate_product()
        )

        if not interesting_dilemmas_product.is_valid():
            logger.error(
                "Was unable to generate interesting dilemmas. Error: %s",
                interesting_dilemmas_product.error(),
            )
            return

        if not interesting_dilemmas_product.get():
            logger.error("No dilemmas have been generated.")
            return

        # Generated interesting dilemmas. Must save them.
        interesting_dilemmas = "\n"

        for interesting_dilemma in interesting_dilemmas_product.get():
            interesting_dilemmas += interesting_dilemma + "\n"

        self._filesystem_manager.append_to_file(
            self._filesystem_manager.get_file_path_to_interesting_dilemmas(
                self._playthrough_name
            ),
            interesting_dilemmas,
        )

        logger.info(
            "Generated interesting dilemmas at '%s'",
            self._filesystem_manager.get_file_path_to_interesting_dilemmas(
                self._playthrough_name
            ),
        )
