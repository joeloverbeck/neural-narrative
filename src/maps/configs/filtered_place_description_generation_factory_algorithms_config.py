from dataclasses import dataclass

from src.maps.algorithms.get_current_weather_identifier_algorithm import (
    GetCurrentWeatherIdentifierAlgorithm,
)
from src.maps.algorithms.get_place_full_data_algorithm import GetPlaceFullDataAlgorithm


@dataclass
class FilteredPlaceDescriptionGenerationFactoryAlgorithmsConfig:
    get_current_weather_identifier_algorithm: GetCurrentWeatherIdentifierAlgorithm
    get_place_full_data_algorithm: GetPlaceFullDataAlgorithm
