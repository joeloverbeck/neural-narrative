from typing import Optional

from src.base.validators import validate_non_empty_string
from src.characters.characters_manager import CharactersManager


class CharacterGenerationInstructionsFormatter:

    def __init__(
        self,
            playthrough_name: str,
            places_descriptions: str,
        templates: dict,
        characters_manager: Optional[CharactersManager] = None,
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._places_descriptions = places_descriptions
        self._templates = templates
        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )

    def format(self) -> str:
        """Formats the character generation instructions with the loaded templates and place parameters."""
        character_generation_instructions = self._templates[
            "character_generation_instructions"
        ]
        formatted_instructions = character_generation_instructions.format(
            places_descriptions=self._places_descriptions,
            prohibited_names=self._characters_manager.get_all_character_names(),
        )
        return formatted_instructions
