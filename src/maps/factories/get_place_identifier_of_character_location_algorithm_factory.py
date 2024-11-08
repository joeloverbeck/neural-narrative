from src.base.validators import validate_non_empty_string
from src.maps.algorithms.get_place_identifier_of_character_location_algorithm import (
    GetPlaceIdentifierOfCharacterLocationAlgorithm,
)


class GetPlaceIdentifierOfCharacterLocationAlgorithmFactory:
    def __init__(self, playthrough_name: str):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._playthrough_name = playthrough_name

    def create_algorithm(
        self, character_identifier: str
    ) -> GetPlaceIdentifierOfCharacterLocationAlgorithm:
        return GetPlaceIdentifierOfCharacterLocationAlgorithm(
            self._playthrough_name, character_identifier
        )
