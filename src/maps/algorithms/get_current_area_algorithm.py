from typing import Optional, Dict, Any

from src.base.constants import PARENT_KEYS
from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_repository import MapRepository


class GetCurrentAreaAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        place_manager_factory: PlaceManagerFactory,
        playthrough_manager: Optional[PlaythroughManager] = None,
        map_repository: Optional[MapRepository] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._place_manager_factory = place_manager_factory

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._map_repository = map_repository or MapRepository(playthrough_name)

    def do_algorithm(self) -> Dict[str, Any]:
        map_file = self._map_repository.load_map_data()

        place_manager = self._place_manager_factory.create_place_manager()

        current_place_type = place_manager.get_current_place_type()

        current_place_identifier = (
            self._playthrough_manager.get_current_place_identifier()
        )

        if current_place_type == TemplateType.AREA:
            return map_file[current_place_identifier]

        if current_place_type == TemplateType.LOCATION:
            current_area_identifier = map_file[current_place_identifier][
                PARENT_KEYS.get(current_place_type)
            ]

            return map_file[current_area_identifier]

        if current_place_type == TemplateType.ROOM:
            current_location_identifier = map_file[current_place_identifier][
                PARENT_KEYS.get(current_place_type)
            ]

            current_area_identifier = map_file[current_location_identifier][
                PARENT_KEYS.get(TemplateType.LOCATION)
            ]

            return map_file[current_area_identifier]

        raise ValueError(f"Not handled for current place type '{current_place_type}'.")
