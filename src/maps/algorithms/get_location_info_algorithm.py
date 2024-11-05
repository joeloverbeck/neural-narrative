from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.algorithms.get_places_in_place_algorithm import GetPlacesInPlaceAlgorithm
from src.maps.data.get_location_info_algorithm_data import (
    GetLocationInfoAlgorithmData,
)


class GetLocationInfoAlgorithm:
    def __init__(
        self,
        get_places_in_place_algorithm: GetPlacesInPlaceAlgorithm,
        get_available_place_types_algorithm: GetAvailablePlaceTypesAlgorithm,
    ):
        self._get_places_in_place_algorithm = get_places_in_place_algorithm
        self._get_available_place_types_algorithm = get_available_place_types_algorithm

    def do_algorithm(self) -> GetLocationInfoAlgorithmData:
        rooms_present = self._get_places_in_place_algorithm.do_algorithm()

        available_room_types = self._get_available_place_types_algorithm.do_algorithm()

        can_search_for_room = bool(available_room_types)

        return GetLocationInfoAlgorithmData(
            rooms_present, can_search_for_room, available_room_types
        )
