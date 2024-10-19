import logging
import os
from typing import Optional

from src.base.abstracts.command import Command
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class AddFactCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        fact: str,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not fact:
            raise ValueError("fact can't be empty.")

        self._playthrough_name = playthrough_name
        self._fact = fact
        self._filesystem_manager = filesystem_manager

    def execute(self) -> None:
        # Could be that the facts file doesn't wist.
        facts_file_path = self._filesystem_manager.get_file_path_to_facts(
            self._playthrough_name
        )

        if not os.path.exists(facts_file_path):
            self._filesystem_manager.write_file(
                facts_file_path,
                "",
            )

        self._filesystem_manager.append_to_file(facts_file_path, self._fact)

        logger.info("Fact added to file.")
