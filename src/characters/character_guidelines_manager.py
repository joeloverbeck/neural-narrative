import logging
from typing import Optional, Dict, List

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import (
    read_json_file,
    write_json_file,
    create_empty_json_file_if_not_exists,
    create_directories,
)
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class CharacterGuidelinesManager:

    def __init__(self, path_manager: Optional[PathManager] = None):
        self._path_manager = path_manager or PathManager()

    def _load_guidelines_file(self) -> Dict[str, List[str]]:
        character_generation_guidelines_path = (
            self._path_manager.get_character_generation_guidelines_path()
        )

        create_directories(self._path_manager.GUIDELINES_DIR)
        create_empty_json_file_if_not_exists(character_generation_guidelines_path)

        return read_json_file(character_generation_guidelines_path)

    def _save_guidelines_file(self, guidelines_file: dict):
        write_json_file(
            self._path_manager.get_character_generation_guidelines_path(),
            guidelines_file,
        )

    @staticmethod
    def create_key(
        story_universe: str,
        world: str,
        region: str,
        area: str,
        location: Optional[str] = None,
    ) -> str:
        return (
            f"{story_universe}:{world}:{region}:{area}:{location}"
            if location
            else f"{story_universe}:{world}:{region}:{area}"
        )

    def load_guidelines(
        self,
        story_universe: str,
        world: str,
        region: str,
        area: str,
        location: Optional[str] = None,
    ) -> List[str]:
        key = self.create_key(story_universe, world, region, area, location)

        logger.info("Guidelines key: %s", key)

        guidelines_file = self._load_guidelines_file()

        if key not in guidelines_file.keys():
            raise ValueError(f"No guidelines found for key '{key}'.")

        return [guideline for guideline in guidelines_file[key]]

    def save_guidelines(
        self,
        story_universe: str,
        world: str,
        region: str,
        area: str,
        guidelines: List[str],
        location: Optional[str] = None,
    ):
        [validate_non_empty_string(guideline, "guideline") for guideline in guidelines]

        key = self.create_key(story_universe, world, region, area, location)

        guidelines_file = self._load_guidelines_file()

        if key not in guidelines_file:
            guidelines_file[key] = [guideline for guideline in guidelines]
        else:
            guidelines_file[key].extend([guideline for guideline in guidelines])

        self._save_guidelines_file(guidelines_file)

    def guidelines_exist(
        self,
        story_universe: str,
        world: str,
        region: str,
        area: str,
        location: Optional[str] = None,
    ) -> bool:
        key = self.create_key(story_universe, world, region, area, location)
        return key in self._load_guidelines_file()
