from typing import Optional, Dict, List

from src.base.constants import CHARACTER_GENERATION_GUIDELINES_FILE
from src.base.required_string import RequiredString
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
    def create_key(
            story_universe: RequiredString,
            world: RequiredString,
            region: RequiredString,
            area: RequiredString,
            location: Optional[RequiredString] = None,
    ) -> RequiredString:
        return RequiredString(
            f"{story_universe.value}:{world.value}:{region.value}:{area.value}:{location.value}"
            if location
            else f"{story_universe.value}:{world.value}:{region.value}:{area.value}"
        )

    def load_guidelines(
            self,
            story_universe: RequiredString,
            world: RequiredString,
            region: RequiredString,
            area: RequiredString,
            location: Optional[RequiredString] = None,
    ) -> List[RequiredString]:
        key = self.create_key(story_universe, world, region, area, location)

        if key.value not in self._guidelines_file:
            raise ValueError(f"No guidelines found for key '{key.value}'.")

        return [
            RequiredString(guideline) for guideline in self._guidelines_file[key.value]
        ]

    def save_guidelines(
        self,
            story_universe: RequiredString,
            world: RequiredString,
            region: RequiredString,
            area: RequiredString,
            guidelines: List[RequiredString],
            location: Optional[RequiredString] = None,
    ):
        key = self.create_key(story_universe, world, region, area, location)

        # Add to the previous guidelines instead of replacing them.
        if key.value not in self._guidelines_file:
            self._guidelines_file[key.value] = [
                guideline.value for guideline in guidelines
            ]
        else:
            # There are already guidelines, so add to the existing ones.
            self._guidelines_file[key.value].extend(
                [guideline.value for guideline in guidelines]
            )

        self._save_guidelines_file()

    def guidelines_exist(
            self,
            story_universe: RequiredString,
            world: RequiredString,
            region: RequiredString,
            area: RequiredString,
            location: Optional[RequiredString] = None,
    ) -> bool:
        key = self.create_key(story_universe, world, region, area, location)

        return key.value in self._guidelines_file
