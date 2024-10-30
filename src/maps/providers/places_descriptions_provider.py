from typing import Optional

from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)


class PlacesDescriptionsProvider:

    def __init__(
        self,
        place_descriptions_for_prompt_factory: PlaceDescriptionsForPromptFactory,
        path_manager: Optional[PathManager] = None,
    ):
        self._place_descriptions_for_prompt_factory = (
            place_descriptions_for_prompt_factory
        )

        self._path_manager = path_manager or PathManager()

    def get_information(self) -> str:
        places_descriptions = read_file(
            self._path_manager.get_places_descriptions_path()
        )
        places_descriptions = places_descriptions.format(
            **self._place_descriptions_for_prompt_factory.create_place_descriptions_for_prompt()
        )
        return places_descriptions
