from src.base.enums import TemplateType
from src.base.playthrough_manager import PlaythroughManager
from src.base.validators import validate_non_empty_string
from src.maps.algorithms.get_area_info_algorithm import GetAreaInfoAlgorithm
from src.maps.algorithms.get_available_place_types_algorithm import (
    GetAvailablePlaceTypesAlgorithm,
)
from src.maps.algorithms.get_places_in_place_algorithm import GetPlacesInPlaceAlgorithm
from src.maps.composers.place_selection_manager_composer import (
    PlaceSelectionManagerComposer,
)
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.navigation_manager_factory import NavigationManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.map_repository import MapRepository


class GetAreaInfoAlgorithmComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_algorithm(self) -> GetAreaInfoAlgorithm:

        current_place_identifier = PlaythroughManager(
            self._playthrough_name
        ).get_current_place_identifier()

        get_places_in_place_algorithm = GetPlacesInPlaceAlgorithm(
            self._playthrough_name,
            current_place_identifier,
            TemplateType.AREA,
            TemplateType.LOCATION,
        )

        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        place_selection_manager = PlaceSelectionManagerComposer(
            self._playthrough_name
        ).compose_manager()

        current_place_template = (
            MapManagerFactory(self._playthrough_name)
            .create_map_manager()
            .get_current_place_template()
        )

        get_available_place_types_algorithm = GetAvailablePlaceTypesAlgorithm(
            self._playthrough_name,
            current_place_template,
            TemplateType.LOCATION,
            place_manager_factory,
            place_selection_manager,
        )

        map_repository = MapRepository(self._playthrough_name)

        navigation_manager_factory = NavigationManagerFactory(map_repository)

        return GetAreaInfoAlgorithm(
            self._playthrough_name,
            current_place_identifier,
            get_places_in_place_algorithm,
            get_available_place_types_algorithm,
            navigation_manager_factory,
        )
