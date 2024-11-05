from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.algorithms.get_location_info_algorithm import GetLocationInfoAlgorithm
from src.maps.algorithms.get_places_in_place_algorithm import GetPlacesInPlaceAlgorithm
from src.maps.composers.place_selection_manager_composer import (
    PlaceSelectionManagerComposer,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class GetLocationInfoAlgorithmComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_algorithm(self) -> GetLocationInfoAlgorithm:
        current_place_identifier = PlaythroughManager(
            self._playthrough_name
        ).get_current_place_identifier()

        get_places_in_place_algorithm = GetPlacesInPlaceAlgorithm(
            self._playthrough_name,
            current_place_identifier,
            TemplateType.LOCATION,
            TemplateType.ROOM,
        )

        place_selection_manager = PlaceSelectionManagerComposer(
            self._playthrough_name
        ).compose_manager()

        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        current_place_template = (
            MapManagerFactory(self._playthrough_name)
            .create_map_manager()
            .get_current_place_template()
        )

        get_available_place_types_algorithm = GetAvailablePlaceTypesAlgorithm(
            self._playthrough_name,
            current_place_template,
            TemplateType.ROOM,
            place_manager_factory,
            place_selection_manager,
        )

        return GetLocationInfoAlgorithm(
            get_places_in_place_algorithm, get_available_place_types_algorithm
        )
