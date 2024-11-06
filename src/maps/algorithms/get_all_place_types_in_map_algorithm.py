from typing import List, Dict, Optional

from src.base.enums import TemplateType
from src.base.validators import validate_non_empty_string
from src.maps.map_repository import MapRepository


class GetAllPlaceTypesInMapAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        place_type: TemplateType,
        map_repository: Optional[MapRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._place_type = place_type

        self._map_repository = map_repository or MapRepository(playthrough_name)

    def do_algorithm(self) -> List[Dict[str, str]]:
        """
        Retrieve all places of a type present in the map.

        Returns:
            List[Dict[str, str]]: A list of dictionaries with 'identifier' and 'place_template' keys.
        """
        map_data = self._map_repository.load_map_data()
        places = []
        for identifier, data in map_data.items():
            if data.get("type") == self._place_type.value:
                place_info = {
                    "identifier": identifier,
                    "place_template": data.get("place_template"),
                }
                places.append(place_info)
        return places
