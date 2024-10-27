from typing import Optional, Dict, List

from src.base.validators import validate_non_empty_string
from src.filesystem.file_operations import read_json_file, write_json_file
from src.filesystem.path_manager import PathManager


class CharacterGuidelinesManager:

    def __init__(self, path_manager: Optional[PathManager] = None):
        self._guidelines_file = self._load_guidelines_file()

        self._path_manager = path_manager or PathManager()

    def _load_guidelines_file(self) -> Dict[str, List[str]]:
        return read_json_file(
            self._path_manager.get_character_generation_guidelines_path()
        )

    def _save_guidelines_file(self):
        write_json_file(
            self._path_manager.get_character_generation_guidelines_path(),
            self._guidelines_file,
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

        if key not in self._guidelines_file:
            raise ValueError(f"No guidelines found for key '{key}'.")

        return [guideline for guideline in self._guidelines_file[key]]

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
        if key not in self._guidelines_file:
            self._guidelines_file[key] = [guideline for guideline in guidelines]
        else:
            self._guidelines_file[key].extend([guideline for guideline in guidelines])
        self._save_guidelines_file()

    def guidelines_exist(
        self,
        story_universe: str,
        world: str,
        region: str,
        area: str,
        location: Optional[str] = None,
    ) -> bool:
        key = self.create_key(story_universe, world, region, area, location)
        return key in self._guidelines_file
