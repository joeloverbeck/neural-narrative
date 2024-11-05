from src.base.validators import validate_non_empty_string
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.algorithms.get_places_in_place_algorithm import GetPlacesInPlaceAlgorithm
from src.maps.dataclasses.get_area_info_algorithm_data import GetAreaInfoAlgorithmData
from src.maps.factories.navigation_manager_factory import NavigationManagerFactory


class GetAreaInfoAlgorithm:

    def __init__(
        self,
        playthrough_name: str,
        current_place_identifier: str,
        get_places_in_place_algorithm: GetPlacesInPlaceAlgorithm,
        get_available_place_types_algorithm: GetAvailablePlaceTypesAlgorithm,
        navigation_manager_factory: NavigationManagerFactory,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")
        validate_non_empty_string(current_place_identifier, "current_place_identifier")

        self._playthrough_name = playthrough_name
        self._current_place_identifier = current_place_identifier

        self._get_places_in_place_algorithm = get_places_in_place_algorithm
        self._get_available_place_types_algorithm = get_available_place_types_algorithm
        self._navigation_manager_factory = navigation_manager_factory

    def do_algorithm(self) -> GetAreaInfoAlgorithmData:
        locations_present = self._get_places_in_place_algorithm.do_algorithm()

        cardinal_connections = self._navigation_manager_factory.create_navigation_manager().get_cardinal_connections(
            self._current_place_identifier
        )

        available_location_types = (
            self._get_available_place_types_algorithm.do_algorithm()
        )

        can_search_for_location = bool(available_location_types)

        return GetAreaInfoAlgorithmData(
            locations_present,
            can_search_for_location,
            available_location_types,
            cardinal_connections,
        )
