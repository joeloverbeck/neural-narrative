from typing import Optional

from src.base.constants import PLACES_DESCRIPTIONS_BLOCK
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)


class PlacesDescriptionsProvider:

    def __init__(
        self,
        place_descriptions_for_prompt_factory: PlaceDescriptionsForPromptFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._place_descriptions_for_prompt_factory = (
            place_descriptions_for_prompt_factory
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def get_information(self) -> str:
        places_descriptions = self._filesystem_manager.read_file(
            PLACES_DESCRIPTIONS_BLOCK
        )
        places_descriptions = places_descriptions.format(
            **self._place_descriptions_for_prompt_factory.create_place_descriptions_for_prompt()
        )
        return places_descriptions
