import logging
from typing import List, Dict, Any, Optional

from src.base.abstracts.command import Command
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    create_empty_json_file_if_not_exists,
    read_json_file,
    write_json_file,
)
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class AddMessagesToOngoingDialogueCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        messages: List[Dict[str, Any]],
        playthrough_manager: Optional[PlaythroughManager] = None,
        path_manager: Optional[PathManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name
        self._messages = messages

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )
        self._path_manager = path_manager or PathManager()

    def execute(self) -> None:
        ongoing_dialogue_file_path = self._path_manager.get_ongoing_dialogue_path(
            self._playthrough_name
        )

        if not self._playthrough_manager.has_ongoing_dialogue():
            create_empty_json_file_if_not_exists(ongoing_dialogue_file_path)

        ongoing_dialogue_file = read_json_file(ongoing_dialogue_file_path)

        if not "messages" in ongoing_dialogue_file.keys():
            logger.info("There weren't messages in the ongoing dialogue file.")
            ongoing_dialogue_file["messages"] = []

        for message in self._messages:
            ongoing_dialogue_file["messages"].append(message)

        # Save the dialogue file.
        write_json_file(ongoing_dialogue_file_path, ongoing_dialogue_file)

        logger.info(
            f"Saved ongoing dialogue messages at '{ongoing_dialogue_file_path}'."
        )
