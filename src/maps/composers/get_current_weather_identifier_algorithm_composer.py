from src.base.validators import validate_non_empty_string
from src.maps.algorithms.get_current_area_algorithm import GetCurrentAreaAlgorithm
from src.maps.algorithms.get_current_weather_identifier_algorithm import (
    GetCurrentWeatherIdentifierAlgorithm,
)
from src.maps.factories.place_manager_factory import PlaceManagerFactory


class GetCurrentWeatherIdentifierAlgorithmComposer:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def compose_algorithm(self) -> GetCurrentWeatherIdentifierAlgorithm:
        place_manager_factory = PlaceManagerFactory(self._playthrough_name)

        get_current_area_algorithm = GetCurrentAreaAlgorithm(
            self._playthrough_name, place_manager_factory
        )
        return GetCurrentWeatherIdentifierAlgorithm(get_current_area_algorithm)
