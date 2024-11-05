from src.base.enums import TemplateType
from src.maps.algorithms.get_area_info_algorithm import GetAreaInfoAlgorithm
from src.maps.algorithms.get_location_info_algorithm import GetLocationInfoAlgorithm
from src.maps.dataclasses.get_place_info_algorithm_data import GetPlaceInfoAlgorithmData
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class GetPlaceInfoAlgorithm:

    def __init__(
        self,
        get_area_info_algorithm: GetAreaInfoAlgorithm,
        get_location_info_algorithm: GetLocationInfoAlgorithm,
        place_manager_factory: PlaceManagerFactory,
    ):
        self._get_area_info_algorithm = get_area_info_algorithm
        self._get_location_info_algorithm = get_location_info_algorithm
        self._place_manager_factory = place_manager_factory

    def do_algorithm(self) -> GetPlaceInfoAlgorithmData:
        locations_present = None
        can_search_for_location = False
        available_location_types = []
        rooms_present = None
        can_search_for_room = False
        available_room_types = []
        cardinal_connections = None

        current_place_type = (
            self._place_manager_factory.create_place_manager().get_current_place_type()
        )

        if current_place_type == TemplateType.AREA:
            data = self._get_area_info_algorithm.do_algorithm()
            locations_present = data.locations_present
            available_location_types = data.available_location_types
            can_search_for_location = data.can_search_for_location
            cardinal_connections = data.cardinal_connections

        if current_place_type == TemplateType.LOCATION:
            data = self._get_location_info_algorithm.do_algorithm()
            rooms_present = data.rooms_present
            available_room_types = data.available_room_types
            can_search_for_room = data.can_search_for_room

        return GetPlaceInfoAlgorithmData(
            locations_present,
            can_search_for_location,
            available_location_types,
            cardinal_connections,
            rooms_present,
            can_search_for_room,
            available_room_types,
        )
