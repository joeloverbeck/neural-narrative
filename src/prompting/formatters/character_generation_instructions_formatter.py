from typing import Optional

from src.base.required_string import RequiredString
from src.characters.characters_manager import CharactersManager


class CharacterGenerationInstructionsFormatter:
    def __init__(
        self,
            playthrough_name: RequiredString,
            places_descriptions: RequiredString,
        templates: dict,
        characters_manager: Optional[CharactersManager] = None,
    ):
        self._places_descriptions = places_descriptions
        self._templates = templates

        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )

    def format(
        self,
    ) -> RequiredString:
        """Formats the character generation instructions with the loaded templates and place parameters."""
        character_generation_instructions = self._templates[
            "character_generation_instructions"
        ]

        formatted_instructions = RequiredString(
            character_generation_instructions
        ).value.format(
            places_descriptions=self._places_descriptions.value,
            prohibited_names=self._characters_manager.get_all_character_names(),
        )

        return RequiredString(formatted_instructions)
