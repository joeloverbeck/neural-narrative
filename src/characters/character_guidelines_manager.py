from typing import Optional, Dict, List

from src.base.constants import CHARACTER_GENERATION_GUIDELINES_FILE
from src.base.validators import validate_non_empty_string
from src.filesystem.filesystem_manager import FilesystemManager


class CharacterGuidelinesManager:

    def __init__(self, filesystem_manager: Optional[FilesystemManager] = None):
        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._guidelines_file = self._load_guidelines_file()

    def _load_guidelines_file(self) -> Dict[str, List[str]]:
        return self._filesystem_manager.load_existing_or_new_json_file(
            CHARACTER_GENERATION_GUIDELINES_FILE
        )

    def _save_guidelines_file(self):
        self._filesystem_manager.save_json_file(
            self._guidelines_file, CHARACTER_GENERATION_GUIDELINES_FILE
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
