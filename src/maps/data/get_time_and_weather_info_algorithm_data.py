from dataclasses import dataclass
from typing import List


@dataclass
class GetTimeAndWeatherInfoAlgorithmData:
    current_hour: int
    current_time_of_day: str
    current_weather: str
    current_weather_description: str
    weather_icon_class: str
    all_weathers: List[str]
