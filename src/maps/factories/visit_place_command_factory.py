from src.characters.factories.generate_random_characters_command_factory import (
    GenerateRandomCharactersCommandFactory,
)
from src.movements.commands.visit_place_command import VisitPlaceCommand


class VisitPlaceCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        generate_random_characters_command_factory: GenerateRandomCharactersCommandFactory,
    ):
        self._playthrough_name = playthrough_name
        self._generate_random_characters_command_factory = (
            generate_random_characters_command_factory
        )

    def create_visit_place_command(self, place_identifier: str) -> VisitPlaceCommand:
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        return VisitPlaceCommand(
            self._playthrough_name,
            place_identifier,
            self._generate_random_characters_command_factory,
        )
