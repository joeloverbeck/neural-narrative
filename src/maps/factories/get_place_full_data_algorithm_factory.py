from src.maps.algorithms.get_place_full_data_algorithm import GetPlaceFullDataAlgorithm
from src.maps.factories.hierarchy_manager_factory import HierarchyManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class GetPlaceFullDataAlgorithmFactory:

    def __init__(
        self,
        place_manager_factory: PlaceManagerFactory,
        hierarchy_manager_factory: HierarchyManagerFactory,
    ):
        self._place_manager_factory = place_manager_factory
        self._hierarchy_manager_factory = hierarchy_manager_factory

    def create_algorithm(self, place_identifier: str) -> GetPlaceFullDataAlgorithm:
        return GetPlaceFullDataAlgorithm(
            place_identifier,
            self._place_manager_factory,
            self._hierarchy_manager_factory,
        )
