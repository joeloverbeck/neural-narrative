from src.base.required_string import RequiredString
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.formatters.character_generation_instructions_formatter import (
    CharacterGenerationInstructionsFormatter,
)


class CharacterGenerationInstructionsFormatterFactory:
    def __init__(
            self,
            playthrough_name: RequiredString,
            places_descriptions_provider: PlacesDescriptionsProvider,
    ):
        self._playthrough_name = playthrough_name
        self._places_descriptions_provider = places_descriptions_provider

    def create_formatter(
            self, templates: dict
    ) -> CharacterGenerationInstructionsFormatter:
        return CharacterGenerationInstructionsFormatter(
            self._playthrough_name,
            RequiredString(self._places_descriptions_provider.get_information()),
            templates,
        )
