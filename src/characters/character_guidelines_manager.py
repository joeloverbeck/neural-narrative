from typing import Optional, Dict, List

from src.base.constants import CHARACTER_GENERATION_GUIDELINES_FILE
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
            self._guidelines_file,
            CHARACTER_GENERATION_GUIDELINES_FILE,
        )

    @staticmethod
    def create_key(world: str, region: str, area: str, location: str = None) -> str:
        if not world or not region or not area:
            raise ValueError("World, region, and area can't be empty.")
        return (
            f"{world}:{region}:{area}:{location}"
            if location
            else f"{world}:{region}:{area}"
        )

    def load_guidelines(
        self, world: str, region: str, area: str, location: str = None
    ) -> List[str]:
        key = self.create_key(world, region, area, location)

        if key not in self._guidelines_file:
            raise ValueError(f"No guidelines found for key '{key}'.")

        return self._guidelines_file[key]

    def save_guidelines(
        self,
        world: str,
        region: str,
        area: str,
        guidelines: List[str],
        location: str = None,
    ):
        key = self.create_key(world, region, area, location)

        # Add to the previous guidelines instead of replacing them.
        if key not in self._guidelines_file:
            self._guidelines_file[key] = guidelines
        else:
            # There are already guidelines, so add to the existing ones.
            self._guidelines_file[key].extend(guidelines)

        self._save_guidelines_file()

    def guidelines_exist(
        self, world: str, region: str, area: str, location: str = None
    ) -> bool:
        key = self.create_key(world, region, area, location)

        return key in self._guidelines_file
