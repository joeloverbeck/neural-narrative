from dataclasses import dataclass


@dataclass
class WeatherIdentifier:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError(f"The identifier can't be empty.")
