from src.maps.algorithms.get_current_area_algorithm import GetCurrentAreaAlgorithm


class GetCurrentWeatherIdentifierAlgorithm:
    def __init__(self, get_current_area_algorithm: GetCurrentAreaAlgorithm):
        self._get_current_area_algorithm = get_current_area_algorithm

    def do_algorithm(self) -> str:
        area_data = self._get_current_area_algorithm.do_algorithm()

        if not "weather_identifier" in area_data:
            raise KeyError(
                f"There's no key 'weather_identifier' in area data: {area_data}"
            )

        return area_data["weather_identifier"]
