from pathlib import Path

from src.base.constants import PLACES_DESCRIPTIONS_BLOCK
from src.filesystem.file_operations import read_file
from src.maps.factories.place_descriptions_for_prompt_factory import (
    PlaceDescriptionsForPromptFactory,
)


class PlacesDescriptionsProvider:

    def __init__(
        self,
        place_descriptions_for_prompt_factory: PlaceDescriptionsForPromptFactory,
    ):
        self._place_descriptions_for_prompt_factory = (
            place_descriptions_for_prompt_factory
        )

    def get_information(self) -> str:
        places_descriptions = read_file(Path(PLACES_DESCRIPTIONS_BLOCK))
        places_descriptions = places_descriptions.format(
            **self._place_descriptions_for_prompt_factory.create_place_descriptions_for_prompt()
        )
        return places_descriptions
