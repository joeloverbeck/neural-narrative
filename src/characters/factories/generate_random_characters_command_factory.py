from src.characters.commands.generate_random_characters_command import (
    GenerateRandomCharactersCommand,
)
from src.characters.factories.generate_character_command_factory import (
    GenerateCharacterCommandFactory,
)
from src.maps.places_templates_parameter import PlacesTemplatesParameter


class GenerateRandomCharactersCommandFactory:
    def __init__(
        self,
        playthrough_name: str,
        generate_character_command_factory: GenerateCharacterCommandFactory,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._generate_character_command_factory = generate_character_command_factory

    def create_generate_random_characters_command(
        self, places_templates_parameter: PlacesTemplatesParameter
    ):
        return GenerateRandomCharactersCommand(
            self._playthrough_name,
            places_templates_parameter,
            self._generate_character_command_factory,
        )
