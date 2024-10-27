import logging
import os
from pathlib import Path
from typing import List, Optional

from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class FilesystemManager:

    def __init__(self, path_manager: Optional[PathManager] = None):
        self._path_manager = path_manager or PathManager()

    @staticmethod
    def remove_item_from_file(file_path: Path, index: int):
        """Remove a line at a specific index from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.rstrip("\n") for line in file if line.strip()]
            if 0 <= index < len(lines):
                del lines[index]
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("\n".join(lines))

    def get_playthrough_names(self) -> List[str]:
        playthroughs_folder = self._path_manager.get_playthroughs_path()

        if os.path.exists(playthroughs_folder):
            return [
                name
                for name in os.listdir(playthroughs_folder)
                if os.path.isdir(os.path.join(playthroughs_folder, name))
            ]
        else:
            return []

    def playthrough_exists(self, playthrough_name):
        return playthrough_name in self.get_playthrough_names()

    @staticmethod
    def get_file_path_to_character_image_for_web(
        playthrough_name: str, character_identifier: str
    ):
        return f"playthroughs/{playthrough_name}/images/{character_identifier}.png"
