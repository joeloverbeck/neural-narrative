from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.exceptions import CharacterNotFoundError
from src.maps.map_repository import MapRepository


class GetPlaceIdentifierOfCharacterLocationAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        character_identifier: str,
        map_repository: Optional[MapRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(character_identifier, "character_identifier")

        self._character_identifier = character_identifier

        self._map_repository = map_repository or MapRepository(playthrough_name)

    def do_algorithm(self) -> str:
        map_file = self._map_repository.load_map_data()

        for identifier, data in map_file.items():
            if "characters" in data:
                if self._character_identifier in data["characters"]:
                    return identifier

        raise CharacterNotFoundError(
            f"Couldn't find character '{self._character_identifier}' in the map. Maybe it's the protagonist?"
        )
