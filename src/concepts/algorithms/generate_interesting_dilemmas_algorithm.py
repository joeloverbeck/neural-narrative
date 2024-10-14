import logging
from typing import Optional, List

from src.concepts.factories.interesting_dilemmas_factory import (
    InterestingDilemmasFactory,
)
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class GenerateInterestingDilemmasAlgorithms:
    def __init__(
        self,
        playthrough_name: str,
        interesting_dilemmas_factory: InterestingDilemmasFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._interesting_dilemmas_factory = interesting_dilemmas_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def do_algorithm(self) -> List[str]:

        interesting_dilemmas_product = (
            self._interesting_dilemmas_factory.generate_product()
        )

        if not interesting_dilemmas_product.is_valid():
            error_message = f"Was unable to generate interesting dilemmas. Error: {interesting_dilemmas_product.error()}"
            logger.error(error_message)

            raise ValueError(error_message)

        if not interesting_dilemmas_product.get():
            raise ValueError("No dilemmas have been generated.")

        # Generated interesting dilemmas. Must save them.
        interesting_dilemmas = ""

        for interesting_dilemma in interesting_dilemmas_product.get():
            # Could be that any of the dilemmas isn't valid.
            if interesting_dilemma:
                interesting_dilemmas += "\n" + interesting_dilemma
            else:
                logger.error(
                    f"The generation of interesting dilemmas produced something invalid: {interesting_dilemmas_product.get()}"
                )

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

        return interesting_dilemmas_product.get()
